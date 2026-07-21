from pydantic import BaseModel, Field
from typing import List

class LineItem(BaseModel):
    item_code: str = Field(description="The exact SKU or item identifier")
    quantity: float = Field(description="Number of units")
    unit_price: float = Field(description="Price per individual unit")

class ProcurementDocument(BaseModel):
    document_id: str = Field(description="Unique ID of the document (PO, GRN, or Invoice)")
    po_reference: str = Field(description="The Purchase Order this document refers to")
    items: List[LineItem] = Field(description="List of line items included in the document")

class MatchResult(BaseModel):
    status: str = Field(description="RAG Status: GREEN (Pass), AMBER (Minor Variance), RED (Major Variance)")
    discrepancies: List[str] = Field(default_factory=list, description="Specific deterministic variance reasons")
    requires_human_review: bool = Field(default=False, description="Flag for ERP routing")