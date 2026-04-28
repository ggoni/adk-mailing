from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.db.database import SessionLocal
from app.services.clustering import ClusteringService
from app.services.orchestrator import OrchestratorService

router = APIRouter()

@router.post("/campaign/run")
async def run_campaign_pipeline():
    try:
        # Run clustering
        cluster_svc = ClusteringService()
        num_clusters = cluster_svc.run_clustering()
        
        # Run orchestrator
        orchestrator_svc = OrchestratorService()
        generated_count = await orchestrator_svc.run_orchestration()
        
        return {
            "status": "success",
            "message": "Pipeline completed successfully",
            "clusters_found": num_clusters,
            "campaigns_generated": generated_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaign/results")
def get_campaign_results():
    db = SessionLocal()
    try:
        query = text("""
            SELECT c.cluster_id, c.generated_text, s.customer_count, s.centroid_features 
            FROM campaign_copy c
            JOIN clusters_summary s ON c.cluster_id = s.id
            ORDER BY c.cluster_id
        """)
        results = db.execute(query).fetchall()
        
        data = []
        for row in results:
            data.append({
                "cluster_id": row[0],
                "generated_text": row[1],
                "customer_count": row[2],
                "centroid_features": row[3]
            })
            
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
