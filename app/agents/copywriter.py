from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from app.core.config import settings

def get_copywriter_agent():
    instruction = """
    Eres un experto redactor de marketing en español chileno.
    Recibirás las características promedio de un segmento de clientes (en formato JSON) en el estado bajo la clave 'cluster_features'.
    Tu tarea es escribir un "Next Best Offer" (texto de campaña por email) de máximo 100 palabras.
    El texto debe ser persuasivo, cercano (usando modismos chilenos sutiles como "po", "cachai" o tuteo adecuado si el grupo es joven, 
    o un trato más formal si es de edad alta o alto patrimonio) y muy enfocado en sus características.
    
    Devuelve ÚNICAMENTE el texto de la campaña, sin saludos iniciales como "Aquí tienes el texto:" ni comillas adicionales.
    """
    
    agent = LlmAgent(
        model=LiteLlm(model="openrouter/anthropic/claude-3.5-sonnet"),
        name="CopywriterAgent",
        instruction=instruction,
        description="Generates marketing copy in Chilean Spanish based on cluster features.",
        output_key="campaign_copy"
    )
    return agent
