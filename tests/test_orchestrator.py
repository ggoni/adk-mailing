import pytest
import asyncio
from unittest.mock import patch, MagicMock
from sqlalchemy import text
from app.services.orchestrator import OrchestratorService
from app.db.database import SessionLocal

@pytest.fixture
def clean_db():
    db = SessionLocal()
    # Insert mock cluster
    db.execute(text("TRUNCATE clusters_summary CASCADE;"))
    db.execute(text("TRUNCATE campaign_copy CASCADE;"))
    db.execute(
        text("INSERT INTO clusters_summary (id, customer_count, centroid_features) VALUES (1, 10, '{\"edad\": 30}')")
    )
    db.commit()
    yield db
    db.execute(text("TRUNCATE clusters_summary CASCADE;"))
    db.execute(text("TRUNCATE campaign_copy CASCADE;"))
    db.commit()
    db.close()

@patch('app.services.orchestrator.Runner')
def test_orchestrator(mock_runner_class, clean_db):
    # Mock Runner instance
    mock_runner = MagicMock()
    
    # We don't really need to mock the event iterator heavily if we mock the whole Runner,
    # but wait, Orchestrator creates its own Runner in __init__.
    # By patching 'Runner' class, the __init__ gets a MagicMock.
    mock_runner_class.return_value = mock_runner
    mock_runner.run.return_value = [] # Return empty events
    
    service = OrchestratorService()
    
    # We also need to mock InMemorySessionService since state checking happens there
    # But InMemorySessionService is local state, so it will actually work!
    # Wait, the code expects the state to have 'campaign_copy' after runner.run().
    # Let's manually inject it into the session before it gets checked.
    async def run_test():
        # Mock get_session to return a predefined state
        async def mock_get_session(app_name, user_id, session_id):
            class MockSession:
                state = {"campaign_copy": "Campaña de prueba."}
            return MockSession()
            
        service.session_service.get_session = mock_get_session
        count = await service.run_orchestration()
        assert count == 1
        
        # Check DB
        res = clean_db.execute(text("SELECT generated_text FROM campaign_copy WHERE cluster_id = 1")).fetchone()
        assert res is not None
        assert res[0] == "Campaña de prueba."

    asyncio.run(run_test())
