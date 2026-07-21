from pydantic_ai import Agent
from src.agents.llm_config import gemma_model

resolution_agent = Agent(
    model=gemma_model,
    system_prompt=(
        "You are an Accounts Payable resolution agent. "
        "Draft a professional vendor email addressing the specific invoice discrepancies provided in the prompt context. "
        "Be concise, firm, and request an amended invoice matching the Goods Received Note (GRN) and Purchase Order (PO) terms."
    )
)