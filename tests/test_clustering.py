import pytest
from sqlalchemy import text
from app.db.database import SessionLocal
from app.services.clustering import ClusteringService

def test_clustering_runs_and_updates_db():
    service = ClusteringService()
    # Using a high eps to ensure some clusters form with standard scaler
    num_clusters = service.run_clustering(eps=2.0, min_samples=5)
    
    db = SessionLocal()
    try:
        # Verify clusters_summary has entries
        summary_count = db.execute(text("SELECT COUNT(*) FROM clusters_summary")).scalar()
        assert summary_count > 0, "No clusters summary generated"
        
        # Verify customers have cluster_ids assigned
        unclustered = db.execute(text("SELECT COUNT(*) FROM customers WHERE cluster_id IS NULL")).scalar()
        assert unclustered == 0, f"Found {unclustered} customers without a cluster_id"
        
    finally:
        db.close()
