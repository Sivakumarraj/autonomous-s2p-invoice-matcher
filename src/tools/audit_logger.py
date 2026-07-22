import sqlite3
import csv
from datetime import datetime
from pathlib import Path

# Define the database path inside a new client_data directory
DB_PATH = Path("client_data/audit_log.db")

def init_db():
    """Initializes the SQLite database and creates the audit table if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Best Practice: Use context manager (with) to prevent memory leaks
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id TEXT,
                po_reference TEXT,
                rag_status TEXT,
                discrepancies TEXT,
                processed_at TIMESTAMP
            )
        """)
        conn.commit()

def log_transaction(invoice_id: str, po_reference: str, rag_status: str, discrepancies: str):
    """Inserts a processed invoice record into the audit log."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoice_audit (invoice_id, po_reference, rag_status, discrepancies, processed_at) VALUES (?, ?, ?, ?, ?)",
            (invoice_id, po_reference, rag_status, discrepancies, datetime.now())
        )
        conn.commit()
    print(f"💾 [AUDIT LOG] Saved {invoice_id} to SQLite database.")

def generate_reconciliation_report(output_path="client_data/daily_reconciliation_report.csv"):
    """Exports the SQLite audit log to a CSV for Accounts Payable review."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_id, po_reference, rag_status, discrepancies, processed_at FROM invoice_audit")
        rows = cursor.fetchall()

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Invoice ID", "PO Reference", "RAG Status", "Discrepancies", "Processed At"])
        writer.writerows(rows)
    
    print(f"📊 [REPORT GENERATED] Daily reconciliation saved to {output_path}")