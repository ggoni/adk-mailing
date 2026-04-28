from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

def get_copywriter_agent():
    instruction = """
    Eres un experto redactor de marketing en español chileno.
    Recibirás las características promedio de un segmento de clientes (en formato JSON) en el siguiente mensaje.
    Tu tarea es escribir un "Next Best Offer" (texto de campaña por email) de máximo 100 palabras.
    El texto debe ser persuasivo, pero no tan cercano (evita usar modismos chilenos sutiles como "po", "cachai" o tuteo 
    aun si el grupo es joven), y optando por un trato más formal si es de edad alta o alto patrimonio) y muy enfocado en sus características.
    Además, IMPORTANTE: redondea todos los montos de dinero (créditos, tarjetas, ingresos) a la centena de mil más cercana (por ejemplo, 1.199.000 a 1.200.000, 250.596 a 300.000, 1.100.528 a 1.100.000).
    OTRA REGLA CRÍTICA: NUNCA menciones los datos personales o demográficos exactos del cliente en el texto (como su edad exacta, meses de antigüedad o el monto exacto de sus ingresos). Solo puedes aludir a esos atributos de forma general (por ejemplo: "basándonos en su trayectoria y estabilidad de ingresos..."). Los ÚNICOS números que tienes permitido imprimir en el correo son los de las ofertas (monto del crédito, cupo de la tarjeta y la tasa de interés).
    
    Devuelve ÚNICAMENTE el texto de la campaña, sin saludos iniciales como "Aquí tienes el texto:" ni comillas adicionales.
    """
    
    agent = LlmAgent(
        model=LiteLlm(model="openrouter/qwen/qwen3.6-flash"),
        name="CopywriterAgent",
        instruction=instruction,
        description="Generates marketing copy in Chilean Spanish based on cluster features.",
        output_key="campaign_copy"
    )
    return agent
