import argparse
import base64
import json
import os
import ssl
import urllib.parse
import urllib.request
from typing import List, Optional, Sequence

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def _encode_username_password(username_password: str) -> str:
    username_password_bytes = username_password.encode("utf-8")
    basic_auth = base64.b64encode(username_password_bytes).strip().decode("utf-8")
    return f"Basic {basic_auth}"


def _get_credentials() -> List[str]:
    credentials_path = os.path.join(os.path.expanduser("~"), ".splunk_kvstore_creds")
    if os.path.exists(credentials_path):
        with open(credentials_path) as f:
            content = f.read()
            credentials = content.strip()
            return credentials.split(";")
    return []


def get_config(app: str, mode: str) -> str:
    host, username_password = _get_credentials()
    url_params = {
        "output_mode": "json",
    }
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{host}/servicesNS/nobody/{app}/storage/collections/config",
            urllib.parse.urlencode(url_params).encode("utf-8"),
            method="GET",
            headers={
                "Authorization": _encode_username_password(username_password),
            },
        ),
        context=ctx,
    )
    response_json = json.load(response)
    if mode == "full":
        return json.dumps(response_json)
    del response_json["links"]
    del response_json["origin"]
    del response_json["updated"]
    del response_json["generator"]
    entries = []
    for entry in response_json["entry"]:
        del entry["id"]
        del entry["links"]
        if entry["acl"]["app"] != "system":
            entries.append(entry)
    return json.dumps(entries)


def get_data(app: str, collection: str) -> str:
    host, username_password = _get_credentials()
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{host}/servicesNS/nobody/{app}/storage/collections/data/{collection}",
            method="GET",
            headers={
                "Authorization": _encode_username_password(username_password),
            },
        ),
        context=ctx,
    )
    response_json = json.load(response)
    return json.dumps(response_json)


def login(username_password: str, host: str) -> None:
    credentials_path = os.path.join(os.path.expanduser("~"), ".splunk_kvstore_creds")
    with open(credentials_path, "w") as f:
        f.write(f"{host};{username_password}\n")
    print(f"Successfully saved credentials to {credentials_path}")


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    login_parser = subparsers.add_parser("login")
    login_parser.add_argument(
        "-c",
        "--creds",
        required=True,
        help="Username and password, in `username:password` format",
    )
    login_parser.add_argument(
        "--host",
        default="https://localhost:8089",
        help="Scheme, host and port, in `scheme://host:port` format",
    )
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("app_collection")
    get_parser.add_argument("-m", "--mode", default="default")
    args = parser.parse_args(argv)
    if args.command == "login":
        login(args.creds, args.host)
    elif args.command == "get":
        if ":" in args.app_collection:
            app, collection = args.app_collection.split(":")
            print(get_data(app, collection))
        else:
            print(get_config(args.app_collection, args.mode))


if __name__ == "__main__":
    main()
