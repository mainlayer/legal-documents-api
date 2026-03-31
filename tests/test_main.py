"""
Test suite for the Legal Documents API.

Runs with no MAINLAYER_API_KEY set, which triggers dev mode (no real payment calls).
"""

from __future__ import annotations

import os
import unittest
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Unset API key so require_payment runs in dev mode.
os.environ.pop("MAINLAYER_API_KEY", None)

from src.main import app  # noqa: E402

AUTH = {"Authorization": "Bearer test-agent-key"}


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


# ---------------------------------------------------------------------------
# Root / health
# ---------------------------------------------------------------------------


class TestMeta:
    def test_health_returns_healthy(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_root_returns_200(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_lists_pricing(self, client: TestClient) -> None:
        body = client.get("/").json()
        assert "pricing" in body
        assert "document_search" in body["pricing"]
        assert "full_document" in body["pricing"]


# ---------------------------------------------------------------------------
# Categories (free endpoint)
# ---------------------------------------------------------------------------


class TestCategories:
    def test_returns_200(self, client: TestClient) -> None:
        resp = client.get("/categories")
        assert resp.status_code == 200

    def test_returns_category_list(self, client: TestClient) -> None:
        body = client.get("/categories").json()
        assert "categories" in body
        assert isinstance(body["categories"], list)
        assert len(body["categories"]) > 0

    def test_total_documents_present(self, client: TestClient) -> None:
        body = client.get("/categories").json()
        assert "total_documents" in body
        assert isinstance(body["total_documents"], int)
        assert body["total_documents"] > 0


# ---------------------------------------------------------------------------
# Document search
# ---------------------------------------------------------------------------


class TestDocumentSearch:
    def test_returns_results_for_contract(self, client: TestClient) -> None:
        resp = client.get("/documents/search", params={"q": "contract"}, headers=AUTH)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_results_have_required_fields(self, client: TestClient) -> None:
        resp = client.get("/documents/search", params={"q": "privacy"}, headers=AUTH)
        assert resp.status_code == 200
        for doc in resp.json():
            assert "id" in doc
            assert "title" in doc
            assert "type" in doc
            assert "jurisdiction" in doc
            assert "relevance_score" in doc

    def test_type_filter(self, client: TestClient) -> None:
        resp = client.get(
            "/documents/search",
            params={"q": "agreement", "type": "contract"},
            headers=AUTH,
        )
        assert resp.status_code == 200
        for doc in resp.json():
            assert doc["type"] == "contract"

    def test_requires_q_parameter(self, client: TestClient) -> None:
        resp = client.get("/documents/search", headers=AUTH)
        assert resp.status_code == 422

    def test_requires_payment_without_key(self, client: TestClient) -> None:
        # Simulate a configured API key that requires auth.
        with patch(
            "src.mainlayer.MainlayerClient.verify_payment",
            new_callable=AsyncMock,
            return_value={"authorized": False, "transaction_id": None, "error": "No funds"},
        ):
            with patch.dict(os.environ, {"MAINLAYER_API_KEY": "real-key-xyz"}):
                # Reset the singleton so it picks up the new key.
                import src.mainlayer as ml_module
                ml_module._client = None
                resp = client.get("/documents/search", params={"q": "test"}, headers=AUTH)
                assert resp.status_code == 402
                ml_module._client = None


# ---------------------------------------------------------------------------
# Get full document
# ---------------------------------------------------------------------------


class TestGetDocument:
    def _get_first_id(self, client: TestClient) -> str:
        results = client.get("/documents/search", params={"q": "agreement"}, headers=AUTH).json()
        assert len(results) > 0, "No documents returned for 'agreement' search"
        return results[0]["id"]

    def test_returns_full_document(self, client: TestClient) -> None:
        doc_id = self._get_first_id(client)
        resp = client.get(f"/documents/{doc_id}", headers=AUTH)
        assert resp.status_code == 200

    def test_full_document_has_text(self, client: TestClient) -> None:
        doc_id = self._get_first_id(client)
        body = client.get(f"/documents/{doc_id}", headers=AUTH).json()
        assert "full_text" in body
        assert len(body["full_text"]) > 0

    def test_not_found_returns_404(self, client: TestClient) -> None:
        resp = client.get("/documents/nonexistent-doc-xyz", headers=AUTH)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Case law search
# ---------------------------------------------------------------------------


class TestCaseLawSearch:
    def test_returns_list(self, client: TestClient) -> None:
        resp = client.get("/cases/search", params={"q": "liability"}, headers=AUTH)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_case_has_required_fields(self, client: TestClient) -> None:
        resp = client.get("/cases/search", params={"q": "contract"}, headers=AUTH)
        assert resp.status_code == 200
        for case in resp.json():
            assert "id" in case
            assert "case_name" in case
            assert "citation" in case
            assert "court" in case
            assert "year" in case
            assert "holding" in case

    def test_requires_q(self, client: TestClient) -> None:
        resp = client.get("/cases/search", headers=AUTH)
        assert resp.status_code == 422

    def test_year_filter_validation(self, client: TestClient) -> None:
        resp = client.get(
            "/cases/search",
            params={"q": "fraud", "year": 1800},
            headers=AUTH,
        )
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Get full case
# ---------------------------------------------------------------------------


class TestGetCase:
    def _get_first_case_id(self, client: TestClient) -> str:
        results = client.get("/cases/search", params={"q": "contract"}, headers=AUTH).json()
        assert len(results) > 0, "No cases returned"
        return results[0]["id"]

    def test_returns_full_case(self, client: TestClient) -> None:
        case_id = self._get_first_case_id(client)
        resp = client.get(f"/cases/{case_id}", headers=AUTH)
        assert resp.status_code == 200

    def test_full_case_has_reasoning(self, client: TestClient) -> None:
        case_id = self._get_first_case_id(client)
        body = client.get(f"/cases/{case_id}", headers=AUTH).json()
        assert "reasoning" in body
        assert "holding" in body

    def test_not_found_returns_404(self, client: TestClient) -> None:
        resp = client.get("/cases/nonexistent-case-xyz", headers=AUTH)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------


class TestTemplates:
    def test_nda_template(self, client: TestClient) -> None:
        resp = client.get("/templates/nda", headers=AUTH)
        assert resp.status_code == 200

    def test_saas_agreement_template(self, client: TestClient) -> None:
        resp = client.get("/templates/saas_agreement", headers=AUTH)
        assert resp.status_code == 200

    def test_template_has_text(self, client: TestClient) -> None:
        body = client.get("/templates/nda", headers=AUTH).json()
        assert "template_text" in body
        assert len(body["template_text"]) > 0

    def test_template_has_sections(self, client: TestClient) -> None:
        body = client.get("/templates/nda", headers=AUTH).json()
        assert "sections" in body
        assert isinstance(body["sections"], list)
        assert len(body["sections"]) > 0

    def test_invalid_template_type_returns_404(self, client: TestClient) -> None:
        resp = client.get("/templates/invalid_template_xyz", headers=AUTH)
        assert resp.status_code == 404
