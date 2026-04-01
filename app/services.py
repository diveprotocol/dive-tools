from urllib.parse import urlparse
from .models import DiveCheckResult
from .utils import normalize_url
from opendive.dns import get_dive_record_walk, get_key_record_walk, DiveRecordNotFound

def check_dive_protection(url: str, require_dnssec: bool = True) -> DiveCheckResult:
    """
    Check if a URL is protected by DIVE.
    Does not download the resource, only checks DNS records.
    """
    result = DiveCheckResult(url=url, is_protected=False)
    normalized_url = normalize_url(url)
    if not normalized_url:
        result.error = "Invalid URL"
        return result

    try:
        parsed = urlparse(normalized_url)
        fqdn = parsed.netloc
    except Exception as e:
        result.error = f"URL parsing failed: {str(e)}"
        return result

    # Check for _dive policy record
    try:
        policy_records = get_dive_record_walk(fqdn)
        if not policy_records:
            return result  # No DIVE policy

        policy = policy_records[0]
        result.is_protected = True
        result.scope = policy.get("scopes", [None])[0] if policy.get("scopes") else None
        result.policy_domain = policy.get("_fqdn", "").replace("_dive.", "")
        result.policy_fqdn = fqdn
        result.directives = policy.get("directives", [])

        # DNSSEC is valid only if ALL records in the chain are validated
        result.dnssec_validated = all(
            record.get("_dnssec_validated", False) for record in policy_records
        )

        # Check for keys if scopes are defined
        if result.scope:
            scopes = policy.get("scopes", [])
            if scopes:
                try:
                    keys = get_key_record_walk(fqdn, "key1")  # Example: check for "key1"
                    result.keys = [
                        {
                            "key_id": key.get("_key_id"),
                            "algorithm": key.get("sig"),
                            "fqdn": key.get("_fqdn"),
                            "dnssec_validated": key.get("_dnssec_validated", False),
                        }
                        for key in keys
                    ]

                    # DNSSEC of keys must also be consistent with the policy chain
                    if result.keys:
                        keys_dnssec = all(k["dnssec_validated"] for k in result.keys)
                        result.dnssec_validated = result.dnssec_validated and keys_dnssec

                except DiveRecordNotFound:
                    pass  # No keys found (but policy exists, so still protected)

    except Exception as e:
        result.error = f"DIVE check failed: {str(e)}"

    return result
