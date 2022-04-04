import json
import os

import splunk_kvstore_cli

SPLUNK_USERNAME = "admin"
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")


def test_kv_login():
    splunk_kvstore_cli.login(
        f"{SPLUNK_USERNAME}:{SPLUNK_PASSWORD}", host="https://localhost:8089"
    )
    credentials_path = os.path.join(os.path.expanduser("~"), ".splunk_kvstore_creds")
    with open(credentials_path) as f:
        content = f.read()
    assert f"https://localhost:8089;admin:{SPLUNK_PASSWORD}\n" == content


def test_kv_get_config_when_no_collection():
    splunk_kvstore_cli.login(
        f"{SPLUNK_USERNAME}:{SPLUNK_PASSWORD}", host="https://localhost:8089"
    )
    result = splunk_kvstore_cli.get_config("search", "default")
    parsed = json.loads(result)
    assert len(parsed) == 1
