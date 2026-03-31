# Legal Documents API

Legal documents and case law sold per document to AI agents via [Mainlayer](https://mainlayer.fr) payment infrastructure.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/categories` | free | List all document categories |
| GET | `/documents/search?q=` | $0.003 | Search legal documents |
| GET | `/documents/{id}` | $0.050 | Retrieve full document text |
| GET | `/cases/search?q=` | $0.010 | Search case law |
| GET | `/cases/{id}` | $0.050 | Retrieve full judicial opinion |
| GET | `/templates/{type}` | $0.020 | Download legal template |
| GET | `/health` | free | Health check |

Available template types: `nda`, `saas_agreement`, `employment_agreement`, `independent_contractor`

## Authentication

All paid endpoints require a Mainlayer API key:

```
Authorization: Bearer <your_mainlayer_api_key>
```

Get your API key at [mainlayer.fr](https://mainlayer.fr).

## Quick Start

```python
import httpx

headers = {"Authorization": "Bearer YOUR_API_KEY"}

# Search for contract documents
docs = httpx.get(
    "https://legal-api.example.com/documents/search",
    params={"q": "non-disclosure agreement", "type": "contract"},
    headers=headers,
).json()

# Retrieve full case opinion
case = httpx.get(
    "https://legal-api.example.com/cases/case-001",
    headers=headers,
).json()
```

## Running Locally

```bash
pip install -e ".[dev]"
uvicorn src.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## Development Mode

Set `MAINLAYER_API_KEY=""` (unset) to bypass payment validation during local development.

## Running Tests

```bash
pytest tests/ -v
```

## Examples

- [`examples/search_cases.py`](examples/search_cases.py) — Search and retrieve case law
- [`examples/get_contracts.py`](examples/get_contracts.py) — Browse and download contracts and templates
