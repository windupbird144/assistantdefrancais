from collections import defaultdict
from unittest.mock import patch
import pytest


@pytest.fixture(autouse=True)
def mock_config():
    with patch("os.environ", defaultdict(str)):
        yield
