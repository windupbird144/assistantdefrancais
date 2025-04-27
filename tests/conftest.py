from unittest.mock import patch
import pytest


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with patch("assistantdefrancais.telemetry.setup_telemetry"):
        yield
