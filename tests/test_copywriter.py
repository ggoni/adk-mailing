from app.agents.copywriter import get_copywriter_agent
from google.adk.agents import LlmAgent

def test_copywriter_agent_configuration():
    agent = get_copywriter_agent()
    
    # Verifications
    assert isinstance(agent, LlmAgent)
    assert agent.name == "CopywriterAgent"
    assert agent.output_key == "campaign_copy"
    
    # Check that instruction contains key elements
    assert "español chileno" in agent.instruction
    assert "características promedio" in agent.instruction
    
    # Check model wrapper (LiteLlm string representation check is tricky, but we can assert it's configured)
    assert agent.model is not None
