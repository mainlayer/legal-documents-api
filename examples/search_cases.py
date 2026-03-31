"""
Example: Search case law via the Legal Documents API.

Usage:
    export MAINLAYER_API_KEY=your_key_here
    python examples/search_cases.py
"""

import os
import httpx

BASE_URL = os.getenv("LEGAL_API_URL", "http://localhost:8000")
API_KEY = os.getenv("MAINLAYER_API_KEY", "your_api_key_here")

headers = {"Authorization": f"Bearer {API_KEY}"}


def search_cases(query: str, court: str = "", year: int | None = None) -> list:
    """Search case law by keyword, optional court, and optional year."""
    params: dict = {"q": query}
    if court:
        params["court"] = court
    if year:
        params["year"] = year

    resp = httpx.get(f"{BASE_URL}/cases/search", params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_full_case(case_id: str) -> dict:
    """Retrieve full judicial opinion for a case."""
    resp = httpx.get(f"{BASE_URL}/cases/{case_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    # 1. Search for contract dispute cases
    print("=== Searching for 'contract' cases ===")
    cases = search_cases(query="contract")
    print(f"Found {len(cases)} case(s)\n")

    for case in cases[:3]:
        print(f"  [{case['id']}] {case['case_name']}")
        print(f"       Citation: {case['citation']}")
        print(f"       Court: {case['court']} ({case['year']})")
        print(f"       Holding: {case['holding'][:120]}...")
        print(f"       Relevance: {case['relevance_score']:.2f}")
        print()

    # 2. Get full case opinion
    if cases:
        case_id = cases[0]["id"]
        print(f"=== Full opinion: {case_id} ===")
        full = get_full_case(case_id)
        print(f"Case: {full['case_name']}")
        print(f"Court: {full['court']}")
        print(f"Year: {full['year']}")
        print(f"\nFacts:\n{full['facts'][:300]}...\n")
        print(f"Holding:\n{full['holding']}\n")
        print(f"Reasoning:\n{full['reasoning'][:400]}...")
        if full.get("citations_cited"):
            print(f"\nCitations: {', '.join(full['citations_cited'][:3])}")

    # 3. Search filtered by year
    print("\n=== Cases from 2023 ===")
    recent = search_cases(query="liability", year=2023)
    print(f"Found {len(recent)} case(s) from 2023")
    for case in recent[:2]:
        print(f"  {case['case_name']} — {case['court']}")


if __name__ == "__main__":
    main()
