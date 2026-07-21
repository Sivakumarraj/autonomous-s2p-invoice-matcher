# Autonomous AP Matcher: Intake-to-Outcomes Architecture

A production-grade, multi-agent pipeline designed to automate 3-Way Invoice Matching (PO vs. GRN vs. Invoice) using deterministic guardrails. Built to demonstrate resilient, enterprise-scale AI patterns for Source-to-Pay (S2P) platforms.

## 🧠 Architectural Philosophy: Defeating "Agent Debt"
Many GenAI procurement pipelines fail because they rely on probabilistic LLMs to perform exact mathematical matching. This pipeline enforces a strict **Intake-to-Outcomes** paradigm:

1. **Agentic Ingestion (Gemma 4):** Extracts messy, unstructured invoice data (PDF/Email) into strict Pydantic JSON schemas.
2. **Deterministic Validation (Zero-LLM):** Python rule-engines execute the actual 3-way match, enforcing strict organizational tolerance percentages (0% hallucination risk).
3. **Agentic Resolution:** If a variance is detected, a Resolution Agent autonomously drafts vendor-facing clarification emails based on the deterministic discrepancy report.

## ⚙️ Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt