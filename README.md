# DIVE Tools

A Flask-based developer tool to check if a URL is protected by the **DIVE protocol** (Domain-based Integrity Verification Enforcement). Available at [tools.diveprotocol.org](https://tools.diveprotocol.org) and on GitHub: [diveprotocol/dive-tools](https://github.com/diveprotocol/dive-tools).

---

## Features

- Check if a URL is protected by DIVE **without downloading the resource**.
- Retrieve DIVE policy details (scope, directives, DNSSEC status).
- List available keys for the domain.
- Simple web interface for manual checks.
- REST API for programmatic use.

---

## Installation

### Prerequisites

- Python 3.9+
- Pip

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/diveprotocol/dive-tools.git
   cd dive-tools
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python run.py
   ```

   The app will be available at `http://localhost:5000`.

---

## Configuration

Create a `.env` file to override default settings:

```env
SECRET_KEY=your-secret-key
FLASK_DEBUG=True
DNS_RESOLVER=8.8.8.8  # Optional: Custom DNS resolver
REQUIRE_DNSSEC=True   # Require DNSSEC validation
```

---

## API Endpoints

### `GET /`

- Renders the web interface.

### `GET /api/check?url=<url>`

- Check if a URL is protected by DIVE.

**Parameters**:

| Parameter | Type   | Description              |
| --------- | ------ | ------------------------ |
| `url`     | string | URL to check (required). |

**Response**:

```json
{
  "url": "https://example.com",
  "is_protected": true,
  "scope": "strict",
  "policy_domain": "example.com",
  "policy_fqdn": "example.com",
  "dnssec_validated": true,
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

### `POST /api/check`

- Same as `GET /api/check`, but with a JSON body:

  ```json
  {
    "url": "https://example.com"
  }
  ```

---

## Deployment

### With Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### With Docker

A `Dockerfile` and `docker-compose.yml` are already provided in the repository. Build and run with:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`.

---

## Integration

To integrate this tool into the DIVE project website:

1. Deploy the API to a subdomain (e.g., `tools.diveprotocol.org`).
2. Embed the web interface in an iframe or link to it.
3. Use the API endpoint (`/api/check`) for programmatic checks.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
