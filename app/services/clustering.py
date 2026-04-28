import json
import pandas as pd
from sqlalchemy import text
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import DBSCAN
from app.db.database import SessionLocal

class ClusteringService:
    def __init__(self):
        self.features = [
            'edad',
            'ingreso_mensual_clp',
            'antiguedad_cuenta_meses',
            'oferta_credito_clp',
            'tasa_credito_pct',
            'oferta_tc_limite_clp'
        ]

    def run_clustering(self, eps=0.5, min_samples=5):
        db = SessionLocal()
        try:
            # 1. Fetch data
            query = f"SELECT id, {', '.join(self.features)} FROM customers"
            df = pd.read_sql(query, db.get_bind())

            if df.empty:
                print("No data to cluster.")
                return 0

            # 2. Preprocess
            X = df[self.features].copy()
            imputer = SimpleImputer(strategy='mean')
            X_imputed = imputer.fit_transform(X)
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_imputed)

            # 3. DBSCAN
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(X_scaled)
            df['cluster_id'] = clusters

            # Update features back to df for centroid calculation
            X_imputed_df = pd.DataFrame(X_imputed, columns=self.features)
            X_imputed_df['cluster_id'] = clusters

            # 4. Clear old clusters
            db.execute(text("TRUNCATE clusters_summary CASCADE;"))
            
            # Reset clusters on customers
            db.execute(text("UPDATE customers SET cluster_id = NULL;"))

            # 5. Calculate centroids and insert into clusters_summary
            unique_clusters = set(clusters)
            num_clusters = 0

            for c_id in unique_clusters:
                c_data = X_imputed_df[X_imputed_df['cluster_id'] == c_id]
                customer_count = len(c_data)
                
                # Calculate mean for each feature
                centroid = c_data[self.features].mean().to_dict()
                
                # Handle NaNs for JSON serialization
                for k, v in centroid.items():
                    if pd.isna(v):
                        centroid[k] = None
                
                db.execute(
                    text("INSERT INTO clusters_summary (id, customer_count, centroid_features) VALUES (:id, :count, :features)"),
                    {
                        "id": int(c_id),
                        "count": customer_count,
                        "features": json.dumps(centroid)
                    }
                )
                if c_id != -1:
                    num_clusters += 1

            # 6. Update customers table
            updates = [{"c_id": int(row['cluster_id']), "id": int(row['id'])} for _, row in df.iterrows()]
            
            db.execute(
                text("UPDATE customers SET cluster_id = :c_id WHERE id = :id"),
                updates
            )
            
            db.commit()
            print(f"Clustering complete: found {num_clusters} clusters (excluding noise).")
            return num_clusters
        except Exception as e:
            db.rollback()
            print(f"Error during clustering: {e}")
            raise
        finally:
            db.close()

if __name__ == "__main__":
    service = ClusteringService()
    service.run_clustering()
