"""
Example: Search and download legal contracts via the Legal Documents API.

Usage:
    export MAINLAYER_API_KEY=your_key_here
    python examples/get_contracts.py
"""

import os
import httpx

BASE_URL = os.getenv("LEGAL_API_URL", "http://localhost:8000")
API_KEY = os.getenv("MAINLAYER_API_KEY", "your_api_key_here")

headers = {"Authorization": f"Bearer {API_KEY}"}


def list_categories() -> dict:
    """Get all document categories (free endpoint)."""
    resp = httpx.get(f"{BASE_URL}/categories")
    resp.raise_for_status()
    return resp.json()


def search_documents(query: str, doc_type: str = "contract", jurisdiction: str = "") -> list:
    """Search documents by keyword and type."""
    params: dict = {"q": query, "type": doc_type}
    if jurisdiction:
        params["jurisdiction"] = jurisdiction

    resp = httpx.get(f"{BASE_URL}/documents/search", params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_document(doc_id: str) -> dict:
    """Retrieve full document text."""
    resp = httpx.get(f"{BASE_URL}/documents/{doc_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_template(template_type: str) -> dict:
    """Download a legal template (nda, saas_agreement, etc.)."""
    resp = httpx.get(f"{BASE_URL}/templates/{template_type}", headers=headers)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    # 1. Browse available categories (free)
    print("=== Document Categories (free) ===")
    cats = list_categories()
    print(f"Total documents: {cats['total_documents']}")
    for cat in cats["categories"][:4]:
        print(f"  {cat['name']}: {cat['document_count']} documents")
    print()

    # 2. Search for NDA contracts
    print("=== Searching for NDA contracts ===")
    ndas = search_documents(query="non-disclosure", doc_type="contract")
    print(f"Found {len(ndas)} NDA document(s)\n")
    for doc in ndas[:2]:
        print(f"  [{doc['id']}] {doc['title']}")
        print(f"       Jurisdiction: {doc['jurisdiction']}")
        print(f"       Date: {doc['date']}")
        print(f"       Summary: {doc['summary'][:100]}...")
        print()

    # 3. Download full document
    if ndas:
        doc_id = ndas[0]["id"]
        print(f"=== Full document: {doc_id} ===")
        full = get_document(doc_id)
        print(f"Title: {full['title']}")
        print(f"Type: {full['type']} | Jurisdiction: {full['jurisdiction']}")
        print(f"\nDocument text (first 500 chars):")
        print(full["full_text"][:500])
        print("...")

    # 4. Download NDA template
    print("\n=== Downloading NDA Template ===")
    nda_tmpl = get_template("nda")
    print(f"Template: {nda_tmpl['title']}")
    print(f"Jurisdiction: {nda_tmpl['jurisdiction']}")
    print(f"Sections: {', '.join(nda_tmpl['sections'][:4])}")
    print(f"\nTemplate text (first 400 chars):")
    print(nda_tmpl["template_text"][:400])
    print("...")
    print(f"\nNotes: {nda_tmpl['notes']}")

    # 5. Estimate cost
    total_paid_calls = (len(ndas) > 0) + (1 if ndas else 0) + 1  # search + doc + template
    cost = 0.003 + (0.05 if ndas else 0) + 0.02
    print(f"\nTotal API cost: ${cost:.3f} USD ({total_paid_calls} paid calls)")


if __name__ == "__main__":
    main()
