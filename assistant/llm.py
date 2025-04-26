import json
import httpx
from .config import Config


async def get_definition(word: str) -> str:
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
    r = httpx.post(url, headers=headers, data=json.dumps(data))
    final_answer = r.json()["choices"][0]["message"]["content"]
    return final_answer
