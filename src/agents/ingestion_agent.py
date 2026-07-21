from pydantic_ai import Agent
from src.schemas.data_models import ProcurementDocument
from src.agents.llm_config import gemma_model

# The result_type enforces that the LLM MUST return our strict ProcurementDocument schema
ingestion_agent = Agent(
    model=gemma_model, 
    result_type=ProcurementDocument,
    system_prompt=(
        "You are an enterprise procurement ingestion agent. "
        "Extract all invoice line items, prices, and quantities from the raw text into the provided JSON schema. "
        "Do not guess missing values. Respond ONLY with valid JSON. Do not include markdown formatting in your response."
    )
)