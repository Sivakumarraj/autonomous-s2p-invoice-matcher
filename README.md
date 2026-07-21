# Autonomous S2P Invoice Matcher (Intake-to-Outcomes)

A production-grade, multi-agent pipeline designed to automate 3-Way Invoice Matching (Purchase Order vs. Goods Received Note vs. Invoice) using deterministic guardrails. 

Built to demonstrate resilient, enterprise-scale GenAI patterns for **Source-to-Pay (S2P)** platforms.

## 🎯 Why I Built This (The Zycus Merlin Connection)
I built this architecture after researching the **Zycus Merlin Agentic Platform** and the enterprise shift toward **Intake-to-Outcomes (I2O)** in procurement. 

Legacy Source-to-Pay (S2P) systems rely on brittle OCR templates, while early GenAI wrappers rely too heavily on LLMs for financial mathematics. This repository was designed as a Proof-of-Concept to demonstrate how a platform like Zycus Merlin can leverage **Neuro-Symbolic AI**: using fast models (like Gemini 2.5) for unstructured data intake, while keeping core business logic (like 5% price tolerances) locked inside deterministic Python guardrails.

## 🧠 Architectural Philosophy: Defeating "Agent Debt"
Many GenAI procurement pipelines fail in production because they rely on probabilistic LLMs to perform exact mathematical matching and policy enforcement. 

This architecture enforces an **Intake-to-Outcomes (I2O)** paradigm using Neuro-Symbolic AI principles:

1. **Agentic Ingestion (Gemini 2.5 Flash):** An LLM acts as the front door, extracting messy, unstructured vendor invoice text into strict `Pydantic` JSON schemas.
2. **Deterministic Validation (Zero LLM):** Pure Python rule-engines execute the actual 3-way match, enforcing strict organizational tolerance percentages (e.g., 5% price variance). **This eliminates LLM math hallucination risk.**
3. **Agentic Resolution (Gemini 2.5 Flash):** If a variance is detected (Amber/Red status), a Resolution Agent dynamically drafts vendor-facing dispute emails based *only* on the deterministic discrepancy report.

## ⚙️ Architecture Flow
`Unstructured PDF/Email` ➔ `Gemini 2.5 (Extraction)` ➔ `Pydantic Schema Validation` ➔ `Python Math Engine (5% Tolerance)` ➔ `Gemini 2.5 (Resolution Draft)`

## 🚀 Pipeline Execution Output
When a vendor overcharges by 10% and bills for units that never arrived at the warehouse, the pipeline catches it deterministically and drafts the resolution email automatically.

![Pipeline Execution Trace](https://github.com/user-attachments/assets/d7059c0a-0292-45cd-a6c7-5d0b487cd224)

## 🧪 Testing & Reliability
This repository emphasizes robust unit testing for the deterministic tools prior to agent orchestration, ensuring the guardrails function independently of the AI models.

![Pytest Output](https://github.com/user-attachments/assets/a14f8453-a81a-459c-865f-13fd2e323707)

## 🏗 Tech Stack
* **Orchestration Framework:** PydanticAI (Strict JSON schema enforcement)
* **LLM Engine:** Google Gemini 2.5 Flash API (Direct)
* **Validation Layer:** Pure Python (Deterministic Math)
* **Testing:** Pytest

## 💻 Quick Start
```bash
# 1. Clone the repo
git clone [https://github.com/Sivakumarraj/autonomous-s2p-invoice-matcher.git](https://github.com/Sivakumarraj/autonomous-s2p-invoice-matcher.git)
cd autonomous-s2p-invoice-matcher

# 2. Install dependencies
pip install "pydantic-ai-slim[google]" pydantic python-dotenv pytest

# 3. Add your API Key
echo 'GEMINI_API_KEY="your-api-key"' > .env

# 4. Run the Guardrail Tests
python -m pytest tests/ -v

# 5. Execute the Multi-Agent Pipeline
python -m src.pipeline
