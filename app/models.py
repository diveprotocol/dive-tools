from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class DiveCheckResult:
    """Result of a DIVE protection check."""
    url: str
    is_protected: bool
    scope: Optional[str] = None
    policy_domain: Optional[str] = None
    policy_fqdn: Optional[str] = None
    dnssec_validated: bool = False
    directives: Optional[List[str]] = None
    keys: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
