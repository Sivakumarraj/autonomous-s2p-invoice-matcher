from src.schemas.data_models import ProcurementDocument, MatchResult

class ThreeWayMatcher:
    """
    Deterministically compares a Purchase Order (PO), Goods Received Note (GRN), 
    and Vendor Invoice to authorize payment or flag discrepancies.
    """
    def __init__(self, tolerance_percentage: float = 0.05):
        self.tolerance = tolerance_percentage

    def execute_match(self, po: ProcurementDocument, grn: ProcurementDocument, invoice: ProcurementDocument) -> MatchResult:
        discrepancies = []
        
        # 1. Quantity Check (Invoice vs Goods Received)
        inv_quantities = {item.item_code: item.quantity for item in invoice.items}
        grn_quantities = {item.item_code: item.quantity for item in grn.items}
        
        for item_code, inv_qty in inv_quantities.items():
            grn_qty = grn_quantities.get(item_code, 0)
            if inv_qty > grn_qty:
                discrepancies.append(f"Item {item_code}: Billed for {inv_qty}, but only received {grn_qty}.")

        # 2. Price Check (Invoice vs Purchase Order) within Tolerance
        inv_prices = {item.item_code: item.unit_price for item in invoice.items}
        po_prices = {item.item_code: item.unit_price for item in po.items}

        for item_code, inv_price in inv_prices.items():
            po_price = po_prices.get(item_code, 0)
            if po_price > 0:
                variance = (inv_price - po_price) / po_price
                if variance > self.tolerance:
                    discrepancies.append(f"Item {item_code}: Price ${inv_price} exceeds PO price ${po_price} by >{self.tolerance*100}%.")

        # 3. RAG Status Routing
        if not discrepancies:
            return MatchResult(status="GREEN", requires_human_review=False)
        elif len(discrepancies) == 1:
            return MatchResult(status="AMBER", discrepancies=discrepancies, requires_human_review=True)
        else:
            return MatchResult(status="RED", discrepancies=discrepancies, requires_human_review=True)