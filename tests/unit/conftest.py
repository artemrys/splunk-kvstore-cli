import urllib.request
from unittest import mock

import pytest


@pytest.fixture
def mock_urlopen():
    with mock.patch.object(urllib.request, "urlopen") as mck:
        yield mck
