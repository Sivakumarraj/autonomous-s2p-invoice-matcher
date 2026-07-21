import asyncio
from src.schemas.data_models import ProcurementDocument, LineItem
from src.tools.deterministic_match import ThreeWayMatcher
from src.agents.ingestion_agent import ingestion_agent
from src.agents.resolution_agent import resolution_agent

async def run_autonomous_match(raw_invoice_text: str, po_data: ProcurementDocument, grn_data: ProcurementDocument):
    print("\n🚦 1. Running Agentic Ingestion (via Gemma 4)...")
    invoice_data = await ingestion_agent.run(raw_invoice_text)
    
    print("🚦 2. Running Deterministic Match (Zero LLM)...")
    matcher = ThreeWayMatcher(tolerance_percentage=0.05)
    match_result = matcher.execute_match(po=po_data, grn=grn_data, invoice=invoice_data.data)
    
    if match_result.status == "GREEN":
        print("✅ Match Successful. Pushing to ERP.")
        return match_result

    print(f"⚠️  {match_result.status} Status Detected. Running Agentic Resolution...")
    
    resolution_prompt = f"Draft an email to the vendor regarding these discrepancies: {match_result.discrepancies}"
    email_draft = await resolution_agent.run(resolution_prompt)
    
    print("\n📩 Drafted Vendor Email:\n")
    print(email_draft.data)
    return match_result

async def main():
    # MOCK INPUTS
    mock_po = ProcurementDocument(
        document_id="PO-2026-089",
        po_reference="PO-2026-089",
        items=[LineItem(item_code="LPT-THINKPAD-X1", quantity=100, unit_price=1500.00)]
    )

    mock_grn = ProcurementDocument(
        document_id="GRN-8812",
        po_reference="PO-2026-089",
        items=[LineItem(item_code="LPT-THINKPAD-X1", quantity=90, unit_price=1500.00)]
    )

    raw_invoice_text = """
    INVOICE #INV-99213
    Vendor: TechSupply Co.
    Ref PO: PO-2026-089
    
    Items Billed:
    - Code: LPT-THINKPAD-X1
    - Qty: 100
    - Price: $1650.00 (Updated 2026 pricing)
    
    Please pay within 30 days.
    """

    await run_autonomous_match(raw_invoice_text, mock_po, mock_grn)

if __name__ == "__main__":
    asyncio.run(main())