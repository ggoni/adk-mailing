import pytest
from sqlalchemy import text
from app.db.database import SessionLocal

def test_database_connection_and_schema():
    db = SessionLocal()
    try:
        # Test connection
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
        
        # Verify tables exist
        tables = db.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        ).fetchall()
        
        table_names = [table[0] for table in tables]
        assert "customers" in table_names
        assert "clusters_summary" in table_names
        assert "campaign_copy" in table_names
    finally:
        db.close()
