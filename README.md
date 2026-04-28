# Agente de Marketing Inteligente (Smart Marketing Agent)

## Introducción
API de marketing que agrupa a los clientes en segmentos usando DBSCAN. Luego, utiliza un agente de inteligencia artificial (mediante OpenRouter y Google ADK) para redactar campañas de correo electrónico enfocadas a cada perfil, escritas en español chileno con un tono formal y corporativo.

## Stack Tecnológico
- Python 3.11+ (gestión de dependencias con `uv`)
- FastAPI (Backend)
- PostgreSQL (Base de datos vía Docker)
- scikit-learn (Algoritmo DBSCAN para clustering)
- Google ADK + LiteLLM (Orquestación de IA)

## Configuración Inicial (Setup)
1. Copia el archivo `.env.example` a `.env` y configura tu llave `OPENROUTER_API_KEY`.
2. Levanta la base de datos: `docker-compose up -d`
3. Carga los datos iniciales (clientes): `uv run python scripts/seed_data.py`
4. Inicia la API: `uv run uvicorn app.main:app --reload`

## Endpoints
- `POST /api/v1/campaign/run`: Ejecuta el clustering y gatilla los agentes LLM para generar nuevas campañas.
- `GET /api/v1/campaign/results`: Visualiza los textos generados.

## Testing
- Para correr las pruebas unitarias: `uv run pytest`

---

## Runbook / Uso Práctico

### 1. Consultas SQL Útiles (Ejecutables desde la Terminal)
Puedes auditar la base de datos directamente usando el contenedor de Docker, sin necesidad de instalar DBeaver o pgAdmin.

**Ver los textos generados por la Inteligencia Artificial:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT cluster_id, generated_text FROM campaign_copy;"
```

**Ver el tamaño y las características promedio de cada cluster:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT id, customer_count, centroid_features FROM clusters_summary;"
```

**Contar cuántos clientes cayeron en cada cluster:**
```bash
docker exec -it adk-mailing-db psql -U marketing_user -d marketing_db -c "SELECT cluster_id, COUNT(*) FROM customers GROUP BY cluster_id ORDER BY cluster_id;"
```

### 2. Uso de la API (FastAPI)
La forma más expedita de revisar los resultados es levantar el servidor y consultar mediante el navegador o `curl`.

1. **Inicia el servidor local:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

2. **Ver Resultados (Método GET):**
   Abre tu navegador web e ingresa a:
   👉 `http://localhost:8000/api/v1/campaign/results`
   
   O si prefieres usar la terminal:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/campaign/results"
   ```

3. **Ejecutar todo el pipeline desde cero (Método POST):**
   *(Ojo: Esto recalcula los grupos y volverá a consumir tokens de la API de OpenRouter)*
   ```bash
   curl -X POST "http://localhost:8000/api/v1/campaign/run"
   ```
