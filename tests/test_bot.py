from unittest.mock import AsyncMock, patch
from src.bot import definir
import pytest


@pytest.mark.asyncio
async def test_definir_command():
    mock_interaction = AsyncMock()
    mock_interaction.response = AsyncMock()

    with patch("src.bot.get_definition", AsyncMock(return_value="essor")):
        await definir._do_call(mock_interaction, {"mot": "essor"})
        mock_interaction.response.defer.assert_called_once()
        mock_interaction.followup.send.assert_called_once()
        assert "essor" in mock_interaction.followup.send.call_args[0][0]
