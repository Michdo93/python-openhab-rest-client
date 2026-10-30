import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

URL = os.environ.get("OPENHAB_TEST_URL")
TOKEN = os.environ.get("OPENHAB_TEST_TOKEN")


@pytest.fixture(scope="session")
def client():
    if not URL or not TOKEN:
        pytest.skip("OPENHAB_TEST_URL and OPENHAB_TEST_TOKEN not set")
    from openhab import OpenHABClient
    c = OpenHABClient(URL, token=TOKEN)
    assert c.isLoggedIn
    return c
