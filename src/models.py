from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date


class DocumentSearchResult(BaseModel):
    id: str
    title: str
    type: Literal["contract", "case", "statute"]
    jurisdiction: str
    summary: str
    date: str
    relevance_score: float
    cost_usd: float = 0.003


class FullDocument(BaseModel):
    id: str
    title: str
    type: Literal["contract", "case", "statute"]
    jurisdiction: str
    summary: str
    date: str
    parties: Optional[List[str]] = None
    full_text: str
    citations: Optional[List[str]] = None
    tags: List[str] = []
    cost_usd: float = 0.05


class CaseSearchResult(BaseModel):
    id: str
    case_name: str
    citation: str
    court: str
    year: int
    summary: str
    holding: str
    relevance_score: float
    cost_usd: float = 0.01


class FullCase(BaseModel):
    id: str
    case_name: str
    citation: str
    court: str
    year: int
    judges: List[str]
    summary: str
    facts: str
    holding: str
    reasoning: str
    dissent: Optional[str] = None
    citations_cited: List[str] = []
    cited_by: List[str] = []
    tags: List[str] = []
    cost_usd: float = 0.05


class LegalTemplate(BaseModel):
    type: str
    title: str
    description: str
    jurisdiction: str
    last_updated: str
    sections: List[str]
    template_text: str
    notes: str
    cost_usd: float = 0.02


class DocumentCategory(BaseModel):
    id: str
    name: str
    description: str
    document_count: int
    subtypes: List[str]


class CategoriesResponse(BaseModel):
    categories: List[DocumentCategory]
    total_documents: int


class PaymentResponse(BaseModel):
    payment_required: bool
    amount_usd: float
    message: str
    payment_url: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
