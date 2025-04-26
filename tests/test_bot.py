from unittest.mock import AsyncMock
from bot import definir  # The decorated command
import pytest


@pytest.mark.asyncio
async def test_definir_command():
    mock_interaction = AsyncMock()
    mock_interaction.response = AsyncMock()

    await definir._do_call(mock_interaction, {"mot": "essor"})

    mock_interaction.response.send_message.assert_called_once()
    assert "essor" in mock_interaction.response.send_message.call_args[0][0]
