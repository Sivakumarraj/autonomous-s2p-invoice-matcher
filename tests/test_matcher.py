from src.schemas.data_models import ProcurementDocument, LineItem
from src.tools.deterministic_match import ThreeWayMatcher

def test_perfect_match():
    matcher = ThreeWayMatcher()
    po = ProcurementDocument(document_id="PO-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    grn = ProcurementDocument(document_id="GRN-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    inv = ProcurementDocument(document_id="INV-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    
    result = matcher.execute_match(po, grn, inv)
    assert result.status == "GREEN"
    assert result.requires_human_review == False
    assert len(result.discrepancies) == 0

def test_quantity_discrepancy():
    matcher = ThreeWayMatcher()
    po = ProcurementDocument(document_id="PO-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    grn = ProcurementDocument(document_id="GRN-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=8, unit_price=100.0)])
    inv = ProcurementDocument(document_id="INV-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    
    result = matcher.execute_match(po, grn, inv)
    assert result.status == "AMBER" # Only 1 discrepancy triggers AMBER
    assert result.requires_human_review == True
    assert "Billed for 10.0, but only received 8.0" in result.discrepancies[0]

def test_price_tolerance_failure():
    matcher = ThreeWayMatcher(tolerance_percentage=0.05) # 5% tolerance
    po = ProcurementDocument(document_id="PO-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    grn = ProcurementDocument(document_id="GRN-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=100.0)])
    # Vendor charges 110 (10% increase), which exceeds the 5% tolerance
    inv = ProcurementDocument(document_id="INV-1", po_reference="PO-1", items=[LineItem(item_code="A1", quantity=10, unit_price=110.0)])
    
    result = matcher.execute_match(po, grn, inv)
    assert result.status == "AMBER"
    assert "exceeds PO price" in result.discrepancies[0]