# Smart Marketing Agent

## Intro
Marketing API. Clusters users with DBSCAN. Uses Claude 3.5 Sonnet (via OpenRouter & Google ADK) to write Chilean Spanish email copy per cluster.

## Stack
- Python 3.11+ (uv)
- FastAPI
- PostgreSQL (Docker)
- scikit-learn (DBSCAN)
- Google ADK + LiteLLM

## Setup
1. Copy `.env.example` to `.env`. Set `OPENROUTER_API_KEY`.
2. Start DB: `docker-compose up -d`
3. Seed DB: `uv run python scripts/seed_data.py`
4. Run API: `uv run uvicorn app.main:app --reload`

## Endpoints
- `POST /api/v1/campaign/run`: Run DBSCAN and LLM agents.
- `GET /api/v1/campaign/results`: View campaigns.

## Testing
- `uv run pytest`

---

## Runbook / Uso Práctico

### 1. Consultas SQL Útiles (Ejecutables desde Terminal)
Puedes auditar la base de datos directamente usando el contenedor de Docker sin necesidad de instalar DBeaver.

**Ver los textos generados por la IA:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT cluster_id, generated_text FROM campaign_copy;"
```

**Ver el tamaño y características promedio de cada cluster:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT id, customer_count, centroid_features FROM clusters_summary;"
```

**Contar cuántos clientes hay en cada cluster:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT cluster_id, COUNT(*) FROM customers GROUP BY cluster_id ORDER BY cluster_id;"
```

### 2. Uso de la API FastAPI
La forma más sencilla de ver los resultados es iniciar el servidor y usar tu navegador o `curl`.

1. **Inicia el servidor:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

2. **Ver Resultados (Método GET):**
   Abre tu navegador de internet y entra a:
   👉 `http://localhost:8000/api/v1/campaign/results`
   
   O si prefieres usar la terminal:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/campaign/results"
   ```

3. **Ejecutar todo el pipeline de nuevo (Método POST):**
   *(Nota: Esto volverá a consumir tokens de OpenRouter)*
   ```bash
   curl -X POST "http://localhost:8000/api/v1/campaign/run"
   ```
