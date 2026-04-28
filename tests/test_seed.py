import pytest
from sqlalchemy import text
from app.db.database import SessionLocal
from scripts.seed_data import seed_database

def test_seed_data_populates_customers():
    # Run the seed function
    seed_database()
    
    db = SessionLocal()
    try:
        # Check count
        count = db.execute(text("SELECT COUNT(*) FROM customers")).scalar()
        assert count > 0, f"Expected more than 0 rows, got {count}"
        
        # Check some fields
        first_rut = db.execute(text("SELECT rut FROM customers LIMIT 1")).scalar()
        assert first_rut is not None, "RUT should not be None"
    finally:
        db.close()
