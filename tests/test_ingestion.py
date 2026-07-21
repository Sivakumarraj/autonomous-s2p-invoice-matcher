import pytest
from pydantic import ValidationError
from src.schemas.data_models import ProcurementDocument

def test_schema_blocks_llm_hallucinations():
    """
    Simulate the LLM returning bad data types (e.g., a string for quantity).
    This proves our Pydantic schema effectively blocks 'Agent Debt'.
    """
    bad_llm_output = {
        "document_id": "INV-123",
        "po_reference": "PO-456",
        "items": [
            {
                "item_code": "LPT-1", 
                "quantity": "TEN",  # This should be a float!
                "unit_price": 1500.0
            }
        ]
    }
    
    # Pydantic should catch this immediately before it ever reaches our deterministic matcher
    with pytest.raises(ValidationError) as exc_info:
        ProcurementDocument(**bad_llm_output)
    
    assert "Input should be a valid number" in str(exc_info.value)