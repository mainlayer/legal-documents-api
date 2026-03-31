# legal-documents-api

Legal documents and case law sold per document to AI agents via [Mainlayer](https://mainlayer.fr).

## Overview

Pay-per-access API for searching and retrieving contracts, case law, statutes, and legal templates. Each request is billed through Mainlayer's micropayment infrastructure.

**API Docs:** https://legal-api.example.com/docs

## Pricing

| Endpoint | Cost | Use Case |
|----------|------|----------|
| `/documents/search` | $0.003 | Search contracts, statutes, etc. |
| `/documents/{id}` | $0.050 | Retrieve full document text |
| `/cases/search` | $0.010 | Search case law by topic/court |
| `/cases/{id}` | $0.050 | Get full judicial opinion + citations |
| `/templates/{type}` | $0.020 | Download pre-reviewed legal templates |
| `/categories` | FREE | List all document categories |

## Agent Example: Pay-Per-Document

```python
from mainlayer import MainlayerClient
import httpx

client = MainlayerClient(api_key="sk_test_...")
token = client.get_access_token("legal-documents-api")
headers = {"Authorization": f"Bearer {token}"}

# Search ($0.003)
results = httpx.get(
    "https://legal-api.example.com/documents/search",
    params={"q": "software licensing", "type": "contract"},
    headers=headers
).json()

# Retrieve one full document ($0.050)
doc = httpx.get(
    f"https://legal-api.example.com/documents/{results[0]['id']}",
    headers=headers
).json()
print(doc["full_text"])
```

## Available Template Types

- `nda` — Non-Disclosure Agreement
- `saas_agreement` — SaaS Terms of Service
- `employment_agreement` — Employment Contract
- `independent_contractor` — 1099 Contractor Agreement

## Install & Run

```bash
pip install -e ".[dev]"
uvicorn src.main:app --reload

# Open http://localhost:8000/docs
pytest tests/ -v
```

## Environment Variables

```
MAINLAYER_API_KEY      # Your Mainlayer API key
MAINLAYER_RESOURCE_ID  # Resource ID from Mainlayer dashboard
CORS_ORIGINS           # CORS-allowed origins (default: *)
LOG_LEVEL              # Logging level (default: INFO)
```

## Development

Set `MAINLAYER_API_KEY=""` to bypass payment during local development.

📚 [Mainlayer Docs](https://docs.mainlayer.fr) | [mainlayer.fr](https://mainlayer.fr)
