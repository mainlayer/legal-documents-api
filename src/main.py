"""
Legal Documents API
-------------------
Pay-per-document access to contracts, case law, statutes, and legal templates.
Powered by Mainlayer — Stripe for AI agents.
"""

import logging
import os
from typing import Optional, List, Literal

from fastapi import FastAPI, Query, Path, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import (
    DocumentSearchResult,
    FullDocument,
    CaseSearchResult,
    FullCase,
    LegalTemplate,
    DocumentCategory,
    CategoriesResponse,
    ErrorResponse,
)
from .legal_db import (
    search_documents,
    get_document,
    search_cases,
    get_case,
    get_template,
    get_categories,
)
from .mainlayer import require_payment

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Legal Documents API",
    description=(
        "Legal documents and case law with pay-per-document access. "
        "Search contracts, statutes, case law, and legal templates. "
        "Powered by Mainlayer — the payments layer for AI agents."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={"name": "Mainlayer Support", "url": "https://api.mainlayer.fr"},
    license_info={"name": "Commercial", "url": "https://api.mainlayer.fr/legal"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        body = exc.detail
    else:
        body = {"error": str(exc.detail), "detail": str(exc.detail), "status_code": exc.status_code}
    return JSONResponse(status_code=exc.status_code, content=body)


# ---------------------------------------------------------------------------
# Root / health
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Legal Documents API",
        "version": "1.0.0",
        "description": "Pay-per-document access to legal documents and case law",
        "docs": "/docs",
        "pricing": {
            "document_search": "$0.003 per search",
            "full_document": "$0.05 per document",
            "case_search": "$0.01 per search",
            "full_case": "$0.05 per case",
            "legal_template": "$0.02 per template",
            "categories": "FREE",
        },
        "auth": "Authorization: Bearer <api_key>",
        "info": "https://api.mainlayer.fr",
    }


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy", "service": "legal-documents-api"}


# ---------------------------------------------------------------------------
# FREE endpoints
# ---------------------------------------------------------------------------

@app.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="List document categories",
    description="Returns all available document categories and their metadata. This endpoint is FREE.",
    tags=["Categories"],
)
async def list_categories() -> CategoriesResponse:
    raw = get_categories()
    categories = [DocumentCategory(**c) for c in raw]
    total = sum(c.document_count for c in categories)
    return CategoriesResponse(categories=categories, total_documents=total)


# ---------------------------------------------------------------------------
# PAID endpoints — Documents
# ---------------------------------------------------------------------------

@app.get(
    "/documents/search",
    response_model=List[DocumentSearchResult],
    summary="Search legal documents",
    description=(
        "Search across contracts, statutes, and other legal documents. "
        "Supports filtering by document type and jurisdiction. "
        "**Cost: $0.003 per search.**"
    ),
    tags=["Documents"],
    responses={
        402: {"description": "Payment required — add funds to your Mainlayer account"},
        200: {"description": "Search results"},
    },
)
async def search_legal_documents(
    request: Request,
    q: str = Query(..., description="Search query", min_length=1, max_length=500),
    type: Optional[Literal["contract", "case", "statute"]] = Query(
        None, description="Filter by document type"
    ),
    jurisdiction: Optional[str] = Query(
        None, description="Filter by jurisdiction (e.g. US-CA, US-NY, EU)", max_length=20
    ),
) -> List[DocumentSearchResult]:
    await require_payment(
        request,
        amount_usd=0.003,
        resource_id=f"doc-search:{q[:40]}",
        resource_type="document_search",
    )

    raw = search_documents(q=q, doc_type=type, jurisdiction=jurisdiction)

    return [
        DocumentSearchResult(
            id=d["id"],
            title=d["title"],
            type=d["type"],
            jurisdiction=d["jurisdiction"],
            summary=d["summary"],
            date=d["date"],
            relevance_score=d["relevance_score"],
        )
        for d in raw
    ]


@app.get(
    "/documents/{id}",
    response_model=FullDocument,
    summary="Retrieve full legal document",
    description=(
        "Retrieve the complete text of a legal document by ID. "
        "**Cost: $0.05 per document.**"
    ),
    tags=["Documents"],
    responses={
        402: {"description": "Payment required"},
        404: {"description": "Document not found"},
    },
)
async def get_legal_document(
    request: Request,
    id: str = Path(..., description="Document ID", example="doc-001"),
) -> FullDocument:
    await require_payment(
        request,
        amount_usd=0.05,
        resource_id=f"doc:{id}",
        resource_type="full_document",
    )

    doc = get_document(id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{id}' not found")

    return FullDocument(
        id=doc["id"],
        title=doc["title"],
        type=doc["type"],
        jurisdiction=doc["jurisdiction"],
        summary=doc["summary"],
        date=doc["date"],
        parties=doc.get("parties"),
        full_text=doc["full_text"],
        citations=doc.get("citations"),
        tags=doc.get("tags", []),
    )


# ---------------------------------------------------------------------------
# PAID endpoints — Cases
# ---------------------------------------------------------------------------

@app.get(
    "/cases/search",
    response_model=List[CaseSearchResult],
    summary="Search case law",
    description=(
        "Search published court opinions. Filter by court name and year. "
        "**Cost: $0.01 per search.**"
    ),
    tags=["Cases"],
    responses={
        402: {"description": "Payment required"},
    },
)
async def search_case_law(
    request: Request,
    q: str = Query(..., description="Search query", min_length=1, max_length=500),
    court: Optional[str] = Query(
        None, description="Filter by court (e.g. '9th Circuit', 'S.D.N.Y.')", max_length=100
    ),
    year: Optional[int] = Query(
        None, description="Filter by decision year", ge=1900, le=2100
    ),
) -> List[CaseSearchResult]:
    await require_payment(
        request,
        amount_usd=0.01,
        resource_id=f"case-search:{q[:40]}",
        resource_type="case_search",
    )

    raw = search_cases(q=q, court=court, year=year)

    return [
        CaseSearchResult(
            id=c["id"],
            case_name=c["case_name"],
            citation=c["citation"],
            court=c["court"],
            year=c["year"],
            summary=c["summary"],
            holding=c["holding"],
            relevance_score=c["relevance_score"],
        )
        for c in raw
    ]


@app.get(
    "/cases/{id}",
    response_model=FullCase,
    summary="Retrieve full case opinion",
    description=(
        "Retrieve the complete judicial opinion including facts, holding, reasoning, "
        "citations, and any dissents. **Cost: $0.05 per case.**"
    ),
    tags=["Cases"],
    responses={
        402: {"description": "Payment required"},
        404: {"description": "Case not found"},
    },
)
async def get_case_opinion(
    request: Request,
    id: str = Path(..., description="Case ID", example="case-001"),
) -> FullCase:
    await require_payment(
        request,
        amount_usd=0.05,
        resource_id=f"case:{id}",
        resource_type="full_case",
    )

    case = get_case(id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{id}' not found")

    return FullCase(
        id=case["id"],
        case_name=case["case_name"],
        citation=case["citation"],
        court=case["court"],
        year=case["year"],
        judges=case["judges"],
        summary=case["summary"],
        facts=case["facts"],
        holding=case["holding"],
        reasoning=case["reasoning"],
        dissent=case.get("dissent"),
        citations_cited=case.get("citations_cited", []),
        cited_by=case.get("cited_by", []),
        tags=case.get("tags", []),
    )


# ---------------------------------------------------------------------------
# PAID endpoints — Templates
# ---------------------------------------------------------------------------

VALID_TEMPLATE_TYPES = ["nda", "saas_agreement", "employment_agreement", "independent_contractor"]


@app.get(
    "/templates/{type}",
    response_model=LegalTemplate,
    summary="Retrieve legal template",
    description=(
        "Download an attorney-reviewed legal template. Available types: "
        "`nda`, `saas_agreement`, `employment_agreement`, `independent_contractor`. "
        "**Cost: $0.02 per template.**"
    ),
    tags=["Templates"],
    responses={
        402: {"description": "Payment required"},
        404: {"description": "Template type not found"},
    },
)
async def get_legal_template(
    request: Request,
    type: str = Path(
        ...,
        description="Template type",
        example="nda",
    ),
) -> LegalTemplate:
    if type not in VALID_TEMPLATE_TYPES:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Template type '{type}' not found. "
                f"Available types: {', '.join(VALID_TEMPLATE_TYPES)}"
            ),
        )

    await require_payment(
        request,
        amount_usd=0.02,
        resource_id=f"template:{type}",
        resource_type="legal_template",
    )

    tmpl = get_template(type)
    if not tmpl:
        raise HTTPException(status_code=404, detail=f"Template '{type}' not found")

    return LegalTemplate(
        type=tmpl["type"],
        title=tmpl["title"],
        description=tmpl["description"],
        jurisdiction=tmpl["jurisdiction"],
        last_updated=tmpl["last_updated"],
        sections=tmpl["sections"],
        template_text=tmpl["template_text"],
        notes=tmpl["notes"],
    )
