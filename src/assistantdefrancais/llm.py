import asyncio
import json
import time
import httpx
from .config import Config
from opentelemetry import metrics
from opentelemetry import trace


tracer = trace.get_tracer(__name__)


meter = metrics.get_meter("llm")
meter_duration = meter.create_counter(
    "llm.duration", description="Time spent on LLM API calls", unit="s"
)
meter_cost = meter.create_counter("llm.cost")
counter_invocations = meter.create_counter("llm.call.count")


async def get_definition(word: str) -> str:
    start = time.perf_counter()
    model = Config.OPENROUTER_MODEL
    prompt = f"""
    Donne une définition complète et détaillée du mot '{word}' en français. Incluse le genre du nom (m. ou f.), la définition, et un exemple de phrase utilisant le mot. Utilise le format suivant : <mot> (<genre>) : <définition>.

    Exemple :
    maison (f.) : Bâtiment d’habitation ; construction faite pour être habitée.
    Exemple : Ils ont acheté une nouvelle maison à la campagne.

    Réponds uniquement selon ce format exact, sans commentaires supplémentaires, titres, ou tout autre texte."""
    llm_response = None
    with tracer.start_as_current_span("llm.get_definition") as span:
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.prompt", prompt)
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": Config.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
        response = httpx.post(
            Config.OPENROUTER_API_URL, headers=headers, data=json.dumps(data)
        )
        span.set_attribute("http.status_code", response.status_code)
        try:
            response.raise_for_status()
            response_body = response.json()
            generation_id = response_body["id"]
            try:
                generation_info = await get_generation(generation_id)
                total_cost = generation_info["data"]["total_cost"]
                span.set_attribute("llm.cost", total_cost)
                meter_cost.add(total_cost, {"llm.model": model})
            except Exception as exc:
                span.record_exception(exc)
                span.set_attribute("error.type", "llm.fetch_generation")
            span.set_attribute(
                "llm.input_tokens", response_body["usage"]["prompt_tokens"]
            )
            span.set_attribute(
                "llm.output_tokens", response_body["usage"]["completion_tokens"]
            )
            span.set_attribute("http.status_code", response.status_code)
            llm_response = response_body["choices"][0]["message"]["content"]
            span.set_attribute("llm.response", llm_response)
        except httpx.HTTPStatusError as exc:
            span.set_attribute("error", True)
            span.set_attribute("error.type", "http.status_code")
            span.record_exception(exc)
        except httpx.TimeoutException as exc:
            span.set_attribute("error", True)
            span.set_attribute("error.type", "http.timeout")
            span.record_exception(exc)
        except Exception as exc:
            span.set_attribute("error", True)
            span.record_exception(exc)
        finally:
            elapsed = time.perf_counter() - start
            success = llm_response is not None
            meter_duration.add(elapsed, {"llm.model": model, "success": success})
            counter_invocations.add(
                1,
                {
                    "llm.model": model,
                    "success": success,
                },
            )
            return llm_response


async def get_generation(generation_id: int):
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    for attempt in range(2):
        response = httpx.get(
            Config.OPENROUTER_GENERATION_API_URL,
            headers=headers,
            params={"id": generation_id},
        )
        if response.status_code == 200:
            break
        else:
            await asyncio.sleep(0.5)
    response.raise_for_status()
    response_body = response.json()
    return response_body
