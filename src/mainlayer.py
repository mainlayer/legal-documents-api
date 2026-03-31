"""
Mainlayer payment integration — Stripe for AI agents.
Handles pay-per-request billing via the Mainlayer API.
Base URL: https://api.mainlayer.xyz
"""

import os
import httpx
import logging
from typing import Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

MAINLAYER_BASE_URL = "https://api.mainlayer.xyz"
MAINLAYER_API_KEY = os.getenv("MAINLAYER_API_KEY", "")
SERVICE_ID = os.getenv("MAINLAYER_SERVICE_ID", "legal-documents-api")


class MainlayerClient:
    """Client for interacting with the Mainlayer billing API."""

    def __init__(self, api_key: str = MAINLAYER_API_KEY, base_url: str = MAINLAYER_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def verify_payment(
        self,
        request: Request,
        amount_usd: float,
        resource_id: str,
        resource_type: str,
    ) -> dict:
        """
        Verify that the caller has paid (or authorize a charge) for the requested resource.
        Returns a dict with keys: authorized (bool), transaction_id (str | None), error (str | None).
        """
        if not self.api_key:
            # Dev mode — no key configured, allow all requests
            logger.warning("MAINLAYER_API_KEY not set — running in unauthenticated dev mode")
            return {"authorized": True, "transaction_id": "dev-mode", "error": None}

        caller_key = _extract_bearer(request)
        if not caller_key:
            return {
                "authorized": False,
                "transaction_id": None,
                "error": "Missing Authorization header. Provide: Authorization: Bearer <api_key>",
            }

        payload = {
            "service_id": SERVICE_ID,
            "resource_id": resource_id,
            "resource_type": resource_type,
            "amount_usd": amount_usd,
            "caller_api_key": caller_key,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{self.base_url}/v1/authorize",
                    json=payload,
                    headers=self.headers,
                )
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "authorized": data.get("authorized", False),
                    "transaction_id": data.get("transaction_id"),
                    "error": data.get("error"),
                }
            elif resp.status_code == 402:
                return {
                    "authorized": False,
                    "transaction_id": None,
                    "error": "Payment required. Add funds to your Mainlayer account.",
                }
            else:
                logger.error("Mainlayer API error %s: %s", resp.status_code, resp.text)
                return {
                    "authorized": False,
                    "transaction_id": None,
                    "error": f"Payment verification failed (HTTP {resp.status_code})",
                }
        except httpx.TimeoutException:
            logger.error("Mainlayer API timeout")
            return {"authorized": False, "transaction_id": None, "error": "Payment service timeout"}
        except httpx.RequestError as exc:
            logger.error("Mainlayer API request error: %s", exc)
            return {"authorized": False, "transaction_id": None, "error": "Payment service unavailable"}

    async def record_usage(
        self,
        transaction_id: str,
        resource_id: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Record successful resource delivery for analytics."""
        if not self.api_key or transaction_id == "dev-mode":
            return

        payload = {
            "transaction_id": transaction_id,
            "resource_id": resource_id,
            "service_id": SERVICE_ID,
            "metadata": metadata or {},
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    f"{self.base_url}/v1/usage",
                    json=payload,
                    headers=self.headers,
                )
        except Exception as exc:
            # Non-critical — don't fail the request
            logger.warning("Failed to record usage: %s", exc)


def _extract_bearer(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[len("Bearer "):].strip()
        return token if token else None
    return None


# Module-level singleton
_client: Optional[MainlayerClient] = None


def get_mainlayer_client() -> MainlayerClient:
    global _client
    if _client is None:
        _client = MainlayerClient()
    return _client


async def require_payment(
    request: Request,
    amount_usd: float,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Dependency / helper that gates a route behind Mainlayer payment.
    Returns the transaction_id on success.
    Raises HTTPException(402) on payment failure.
    """
    client = get_mainlayer_client()
    result = await client.verify_payment(request, amount_usd, resource_id, resource_type)

    if not result["authorized"]:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment Required",
                "message": result.get("error", "Payment verification failed"),
                "amount_usd": amount_usd,
                "resource_id": resource_id,
                "info": "Visit https://api.mainlayer.xyz to manage your account",
            },
        )

    return result["transaction_id"] or "verified"
