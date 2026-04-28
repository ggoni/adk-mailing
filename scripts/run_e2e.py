import asyncio
from sqlalchemy import text
from app.db.database import SessionLocal
from app.services.clustering import ClusteringService
from app.services.orchestrator import OrchestratorService

async def main():
    print("🚀 Iniciando flujo End-to-End...")
    
    # 1. Clustering
    print("📊 Ejecutando ClusteringService...")
    cluster_svc = ClusteringService()
    num_clusters = cluster_svc.run_clustering()
    print(f"✅ Se encontraron {num_clusters} clusters (excluyendo ruido).")
    
    # 2. Orchestrator
    print("🤖 Ejecutando OrchestratorService (Llamando a Claude 3.5 Sonnet)...")
    orch_svc = OrchestratorService()
    num_campaigns = await orch_svc.run_orchestration()
    print(f"✅ Se generaron {num_campaigns} textos de campaña.")
    
    # 3. Mostrar resultados
    print("\n--- RESULTADOS FINALES ---")
    db = SessionLocal()
    try:
        query = text("""
            SELECT c.cluster_id, s.customer_count, s.centroid_features, c.generated_text
            FROM campaign_copy c
            JOIN clusters_summary s ON c.cluster_id = s.id
            ORDER BY c.cluster_id
        """)
        results = db.execute(query).fetchall()
        for row in results:
            print(f"\n[CLUSTER {row[0]} - {row[1]} clientes]")
            print(f"Características: {row[2]}")
            print("Campaña Generada:")
            print("-" * 40)
            print(row[3])
            print("-" * 40)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
