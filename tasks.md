# Project Task List (MVP)

This document contains a granular, testable MVP task list based on `architecture.md` and `user-stories.md`.

## Task 1: Environment Setup and Database Schema
- **Goal:** Initialize the project using `uv`, set up Docker for PostgreSQL, and define the database schema (SQLAlchemy/SQL).
- **Files to change/create:**
  - `pyproject.toml`
  - `.env.example`
  - `docker-compose.yml`
  - `app/db/schema.sql` (or `app/db/models.py`)
  - `tests/test_db.py`
- **Test(s) to add first:**
  - Write a test connecting to the PostgreSQL database and verifying the creation of `customers`, `clusters_summary`, and `campaign_copy` tables.
- **Implementation steps:**
  1. Initialize the project with `uv init` (Python >= 3.11).
  2. Add dependencies (`fastapi`, `uvicorn`, `psycopg2-binary`, `sqlalchemy`, `scikit-learn`, `pandas`, `adk-python`, `pytest`).
  3. Create `docker-compose.yml` for PostgreSQL.
  4. Create the schema for `customers`, `clusters_summary`, and `campaign_copy`.
- **Definition of Done:** `docker-compose up -d` successfully spins up PostgreSQL, the schema is applied, and `pytest tests/test_db.py` passes.

## Task 2: Mock Data Generator
- **Goal:** Create a script to generate synthetic customer data (e.g., RFM - Recency, Frequency, Monetary) to test the clustering logic.
- **Files to change/create:**
  - `scripts/seed_data.py`
  - `tests/test_seed.py`
- **Test(s) to add first:**
  - Test that the generated data has the correct dimensions, no nulls, and is inserted into the `customers` table correctly.
- **Implementation steps:**
  1. Create a Python script using `numpy` or `pandas` to generate 500+ realistic customer records.
  2. Implement a function to bulk insert this data into PostgreSQL.
- **Definition of Done:** The script runs successfully, populating the `customers` table with mock data, and the test verifies the record count.

## Task 3: DBSCAN Clustering Service
- **Goal:** Implement the analytical pipeline to scale data, apply DBSCAN, and calculate cluster centroids.
- **Files to change/create:**
  - `app/services/clustering.py`
  - `tests/test_clustering.py`
- **Test(s) to add first:**
  - Unit test mocking database input to verify that `StandardScaler` + `DBSCAN` assigns labels properly and identifies noise (cluster `-1`).
  - Unit test to verify centroid calculations.
- **Implementation steps:**
  1. Fetch customer data from the database.
  2. Apply `StandardScaler`.
  3. Apply `DBSCAN` (with a heuristic or static `eps` and `min_samples` for the MVP).
  4. Calculate the average profile for each assigned cluster.
  5. Save results to `clusters_summary` and update customer records.
- **Definition of Done:** Running the service processes the database, assigns a cluster ID to every customer, and `clusters_summary` contains the centroid profiles. All tests pass.

## Task 4: ADK & OpenRouter Agent Configuration
- **Goal:** Configure the `LlmAgent` using Google ADK and OpenRouter to generate the NBO copy.
- **Files to change/create:**
  - `app/agents/copywriter.py`
  - `tests/test_copywriter.py`
- **Test(s) to add first:**
  - Test the `LlmAgent` initialization using `LiteLlm` and OpenRouter credentials.
  - Test the prompt rendering with a mock cluster profile.
- **Implementation steps:**
  1. Initialize `LiteLlm` targeting `openrouter/anthropic/claude-3.5-sonnet`.
  2. Create the `LlmAgent` with instructions for Chilean Spanish and Next Best Offer.
  3. Handle `OPENROUTER_API_KEY` securely from `.env`.
- **Definition of Done:** `pytest tests/test_copywriter.py` verifies the agent is successfully instantiated and returns a mocked response when invoked.

## Task 5: Agent Orchestration and Validation
- **Goal:** Orchestrate the process by iterating over clusters and invoking the ADK Copywriter Agent.
- **Files to change/create:**
  - `app/services/orchestrator.py`
  - `tests/test_orchestrator.py`
- **Test(s) to add first:**
  - Mock the `LlmAgent` execution and verify the orchestrator correctly loops over all valid clusters in `clusters_summary` and saves the results to `campaign_copy`.
- **Implementation steps:**
  1. Fetch all profiles from `clusters_summary`.
  2. For each profile, call the `Copywriter` ADK agent.
  3. Parse the generated copy and save it into the `campaign_copy` table.
- **Definition of Done:** The orchestrator successfully bridges the DB and the ADK Agent, processing all clusters and updating the DB with the generated texts. Tests pass.

## Task 6: FastAPI Endpoints and E2E Integration
- **Goal:** Expose a REST API to trigger the pipeline and retrieve results.
- **Files to change/create:**
  - `app/main.py`
  - `app/api/endpoints.py`
  - `tests/test_api.py`
- **Test(s) to add first:**
  - `TestClient` tests for `POST /api/v1/campaign/run` (mocking the background task) and `GET /api/v1/campaign/results`.
- **Implementation steps:**
  1. Setup the FastAPI app.
  2. Create a POST endpoint to trigger the clustering + agent orchestration asynchronously.
  3. Create a GET endpoint to view the generated copies.
- **Definition of Done:** Endpoints return `200 OK`, tasks execute in the background or synchronously for the MVP, and E2E tests confirm the flow from DB to LLM and back to DB.
