import json
import httpx
from .config import Config
import logging
from opentelemetry import metrics

logging.basicConfig(level=logging.DEBUG)


meter = metrics.get_meter("assistant.llm.meter")
get_definition_invocations = meter.create_counter(
    "get_definition.invocations",
    description="How many times get_definition is invoked",
)


async def get_definition(word: str) -> str:
    get_definition_invocations.add(1, {"word": word})
    logging.debug(f"llm: making request for word {word=}")
    url = Config.OPENROUTER_API_URL
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [
            {
                "role": "user",
                "content": f"Donne une définition concise du mot '{word}' en français. Réponds dans le format <mot>: <défitnition>. Réponds uniquement selon le format, sans commentaires supplémentaires.",
            }
        ],
    }
    response = httpx.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_body = response.json()
    logging.debug(f"llm: {response_body=}")
    final_answer = response_body["choices"][0]["message"]["content"]
    return final_answer
