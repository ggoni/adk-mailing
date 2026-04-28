import os
import sys
import argparse
import pandas as pd
from sqlalchemy import text

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.database import SessionLocal

def seed_database(csv_path):
    db = SessionLocal()
    try:
        # Idempotency: clear existing data
        db.execute(text("TRUNCATE customers RESTART IDENTITY CASCADE;"))
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Archivo de datos no encontrado: {csv_path}")
            
        df = pd.read_csv(csv_path)
        
        # Insert data
        for _, row in df.iterrows():
            db.execute(
                text("""INSERT INTO customers (
                    id, rut, nombre, email, sexo, edad, estado_civil, tiene_hijos, profesion, 
                    ingreso_mensual_clp, segmento, es_cliente, antiguedad_cuenta_meses, 
                    conocimiento_inversiones, acepta_comunicaciones, oferta_credito_clp, 
                    tasa_credito_pct, oferta_tc_limite_clp
                ) VALUES (
                    :id, :rut, :nombre, :email, :sexo, :edad, :estado_civil, :tiene_hijos, :profesion,
                    :ingreso_mensual_clp, :segmento, :es_cliente, :antiguedad_cuenta_meses,
                    :conocimiento_inversiones, :acepta_comunicaciones, :oferta_credito_clp,
                    :tasa_credito_pct, :oferta_tc_limite_clp
                )"""),
                {
                    "id": int(row['id']),
                    "rut": str(row['rut']) if pd.notna(row['rut']) else None,
                    "nombre": str(row['nombre']) if pd.notna(row['nombre']) else None,
                    "email": str(row['email']) if pd.notna(row['email']) else None,
                    "sexo": str(row['sexo']) if pd.notna(row['sexo']) else None,
                    "edad": int(row['edad']) if pd.notna(row['edad']) else None,
                    "estado_civil": str(row['estado_civil']) if pd.notna(row['estado_civil']) else None,
                    "tiene_hijos": bool(row['tiene_hijos']) if pd.notna(row['tiene_hijos']) else False,
                    "profesion": str(row['profesion']) if pd.notna(row['profesion']) else None,
                    "ingreso_mensual_clp": float(row['ingreso_mensual_clp']) if pd.notna(row['ingreso_mensual_clp']) else None,
                    "segmento": str(row['segmento']) if pd.notna(row['segmento']) else None,
                    "es_cliente": bool(row['es_cliente']) if pd.notna(row['es_cliente']) else False,
                    "antiguedad_cuenta_meses": float(row['antiguedad_cuenta_meses']) if pd.notna(row['antiguedad_cuenta_meses']) else None,
                    "conocimiento_inversiones": str(row['conocimiento_inversiones']) if pd.notna(row['conocimiento_inversiones']) else None,
                    "acepta_comunicaciones": bool(row['acepta_comunicaciones']) if pd.notna(row['acepta_comunicaciones']) else False,
                    "oferta_credito_clp": float(row['oferta_credito_clp']) if pd.notna(row['oferta_credito_clp']) else None,
                    "tasa_credito_pct": float(row['tasa_credito_pct']) if pd.notna(row['tasa_credito_pct']) else None,
                    "oferta_tc_limite_clp": float(row['oferta_tc_limite_clp']) if pd.notna(row['oferta_tc_limite_clp']) else None
                }
            )
        
        db.commit()
        print(f"Successfully seeded {len(df)} records into the customers table.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed database with customer data.")
    parser.add_argument("--file", "-f", required=True, help="Ruta al archivo CSV de clientes.")
    args = parser.parse_args()
    
    seed_database(args.file)
