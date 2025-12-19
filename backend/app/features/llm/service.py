import httpx


class LlmUnavailableError(Exception):
    """Raised when the LLM endpoint cannot be reached or returns an error."""


async def ask_llm(question: str, base_url: str, model: str) -> str:
    payload = {
        "model": model,
        "prompt": question,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=300) as client:
        try:
            response = await client.post(f"{base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            raise LlmUnavailableError("LLM unavailable or not responding") from exc
