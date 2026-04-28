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
