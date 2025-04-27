import json
from unittest.mock import AsyncMock, patch
from httpx import Response

from assistant.llm import get_definition

import pytest


@pytest.mark.asyncio
async def test_llm_successful_response():
    with patch("httpx.post") as mock_inference:
        with patch("assistant.llm.get_generation") as mock_generation:
            mock_inference.return_value = Response(
                status_code=200,
                content=json.dumps(
                    {
                        "id": "0",
                        "choices": [{"message": {"content": "Hello"}}],
                        "usage": {
                            "prompt_tokens": 0,
                            "completion_tokens": 0,
                        },
                    }
                ),
                request=AsyncMock(),
            )
            mock_generation.return_value = {"data": {"total_cost": 1}}
            response = await get_definition("essor")
            assert response == "Hello"
