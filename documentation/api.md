# DIVE Protection Checker API

**Version**: 1.0
**Base URL**: `/api`
**Authentication**: None (public API)

The DIVE Protection Checker API allows developers to verify if a URL is protected by the DIVE protocol (Domain-based Integrity Verification Enforcement). This API is designed to be integrated into the DIVE project website as a developer tool.

---

## Table of Contents

- [Endpoints](#endpoints)
  - [Check DIVE Protection](#check-dive-protection)
- [Request/Response Examples](#requestresponse-examples)
- [Error Responses](#error-responses)
- [Response Fields](#response-fields)
- [Integration Examples](#integration-examples)
- [Rate Limiting](#rate-limiting)
- [CORS Policy](#cors-policy)

---

## Endpoints

### Check DIVE Protection

**Endpoint**: `GET /api/check`

Verifies if a URL is protected by the DIVE protocol without downloading the resource.

#### Parameters

| Parameter | Type   | Location | Required | Description                      |
| --------- | ------ | -------- | -------- | -------------------------------- |
| `url`     | string | Query    | Yes      | URL to check for DIVE protection |

#### Example Request

```bash
curl "http://yourdomain.com/api/check?url=https://example.com/file.txt"
```

#### Example Response (Success)

```json
{
  "url": "https://example.com/file.txt",
  "is_protected": true,
  "dnssec_validated": true,
  "scope": "strict",
  "policy_domain": "example.com",
  "policy_fqdn": "example.com",
  "directives": ["https-required"],
  "keys": [
    {
      "key_id": "key1",
      "algorithm": "ed25519",
      "fqdn": "key1._divekey.example.com",
      "dnssec_validated": true
    }
  ]
}
```

#### Example Response (Not Protected)

```json
{
  "url": "https://example.com/file.txt",
  "is_protected": false,
  "dnssec_validated": false,
  "error": null
}
```

---

## Request/Response Examples

### Successful DIVE Protection Check

**Request:**

```bash
GET /api/check?url=https://dive-protected.example/file.js
```

**Response:**

```json
{
  "url": "https://dive-protected.example/file.js",
  "is_protected": true,
  "dnssec_validated": true,
  "scope": "strict",
  "policy_domain": "dive-protected.example",
  "policy_fqdn": "dive-protected.example",
  "directives": ["https-required"],
  "keys": [
    {
      "key_id": "production-key",
      "algorithm": "ed25519",
      "fqdn": "production-key._divekey.dive-protected.example",
      "dnssec_validated": true
    }
  ]
}
```

### Domain Without DIVE Protection

**Request:**

```bash
GET /api/check?url=https://regular-example.com/file.txt
```

**Response:**

```json
{
  "url": "https://regular-example.com/file.txt",
  "is_protected": false,
  "dnssec_validated": false,
  "error": null
}
```

### Invalid URL

**Request:**

```bash
GET /api/check?url=invalid-url
```

**Response:**

```json
{
  "error": "Invalid URL"
}
```

---

## Error Responses

The API returns standard HTTP status codes with JSON error responses:

| Status Code | Error Type            | Description                      |
| ----------- | --------------------- | -------------------------------- |
| 400         | Bad Request           | Invalid URL or missing parameter |
| 404         | Not Found             | Endpoint not found               |
| 500         | Internal Server Error | Server-side error                |

**Example Error Response:**

```json
{
  "error": "Invalid URL: please provide a valid HTTP/HTTPS URL"
}
```

---

## Response Fields

| Field                     | Type    | Description                                        |
| ------------------------- | ------- | -------------------------------------------------- |
| `url`                     | string  | The URL that was checked                           |
| `is_protected`            | boolean | Whether the URL is protected by DIVE               |
| `dnssec_validated`        | boolean | Whether DNSSEC validation succeeded                |
| `scope`                   | string  | The DIVE scope (e.g., "strict") if protected       |
| `policy_domain`           | string  | The domain where the DIVE policy is defined        |
| `policy_fqdn`             | string  | The fully qualified domain name                    |
| `directives`              | array   | List of DIVE directives (e.g., ["https-required"]) |
| `keys`                    | array   | List of key records if protected                   |
| `keys[].key_id`           | string  | The key identifier                                 |
| `keys[].algorithm`        | string  | The signature algorithm (e.g., "ed25519")          |
| `keys[].fqdn`             | string  | The FQDN of the key record                         |
| `keys[].dnssec_validated` | boolean | Whether the key record is DNSSEC validated         |
| `error`                   | string  | Error message if the request failed                |

---

## Integration Examples

### JavaScript (Frontend)

```javascript
async function checkDiveProtection(url) {
  try {
    const response = await fetch(`/api/check?url=${encodeURIComponent(url)}`);
    const data = await response.json();

    if (data.error) {
      console.error("Error:", data.error);
      return;
    }

    if (data.is_protected) {
      console.log(`✅ ${url} is protected by DIVE`);
      console.log(`- Scope: ${data.scope}`);
      console.log(
        `- DNSSEC: ${data.dnssec_validated ? "Validated" : "Not validated"}`
      );
      console.log(`- Keys: ${data.keys.length}`);
    } else {
      console.log(`❌ ${url} is NOT protected by DIVE`);
    }

    return data;
  } catch (error) {
    console.error("API request failed:", error);
  }
}

// Example usage
checkDiveProtection("https://example.com/file.js");
```

### Python (Backend)

```python
import requests

def check_dive_protection(url):
    api_url = "http://yourdomain.com/api/check"
    params = {"url": url}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Example usage
result = check_dive_protection("https://example.com/file.txt")
print(result)
```

### cURL (Command Line)

```bash
# Basic check
curl -s "http://yourdomain.com/api/check?url=https://example.com"

# With jq for pretty printing
curl -s "http://yourdomain.com/api/check?url=https://example.com" | jq
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **10 requests per minute per IP address**
- When the limit is exceeded, the API returns HTTP 429 (Too Many Requests)

**Example Response:**

```json
{
  "error": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## CORS Policy

The API supports Cross-Origin Resource Sharing (CORS) for web integration:

- **Allowed Origins**: `*`
- **Allowed Methods**: `GET, OPTIONS`
- **Allowed Headers**: `Content-Type`

This allows the API to be called from any web page, making it easy to integrate with the DIVE project website.

---

## DNS Configuration Notes

For the API to work correctly with your domain:

1. Ensure your DNS zone has proper DNSSEC configuration
2. The `_dive` and `_divekey` records must be properly signed
3. Use a DNS resolver that supports DNSSEC validation (like 8.8.8.8 or 1.1.1.1)

You can verify your DNS configuration with:

```bash
dig +dnssec _dive.yourdomain.com TXT @8.8.8.8
```

---

## Deployment Recommendations

1. **Use HTTPS**: Always deploy the API with HTTPS
2. **Monitor Performance**: The API makes DNS queries which can be slow
3. **Cache Responses**: Consider caching results for frequently checked URLs
4. **DNS Resolver**: Configure the API to use a reliable DNS resolver (8.8.8.8 recommended)

Example configuration for production:

```python
# In your Flask app configuration
app.config.update({
    'DNS_RESOLVER': '8.8.8.8',  # Google DNS
    'REQUIRE_DNSSEC': True      # Enforce DNSSEC validation
})
```

---

## Support

For questions or issues with the API:

- **Email**: support@diveprotocol.org
- **GitHub Issues**: [github.com/diveprotocol/dive-tools/issues](https://github.com/diveprotocol/dive-tools/issues)

---

This API documentation provides everything needed to integrate the DIVE Protection Checker into your website or applications. The API is designed to be simple, reliable, and secure for checking DIVE protocol protection status. 🚀
