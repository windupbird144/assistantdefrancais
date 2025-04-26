import json
from unittest.mock import patch
from httpx import Response

from assistant.llm import get_definition

import pytest


@pytest.mark.asyncio
async def test_llm_successful_response():
    with patch("httpx.post") as mock:
        mock.return_value = Response(
            status_code=200,
            content=json.dumps({"choices": [{"message": {"content": "Hello"}}]}),
        )
        response = await get_definition("essor")
        assert response == "Hello"
