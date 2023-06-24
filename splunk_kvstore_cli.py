import argparse
import base64
import json
import ssl
import urllib.parse
import urllib.request
from typing import Optional, Sequence

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def _encode_username_password(username_password: str) -> str:
    username_password_bytes = username_password.encode("utf-8")
    basic_auth = base64.b64encode(username_password_bytes).strip().decode("utf-8")
    return f"Basic {basic_auth}"


def get_config(creds: str, host: str, addon_name: str, mode: str) -> str:
    url_params = {
        "output_mode": "json",
    }
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{host}/servicesNS/nobody/{addon_name}/storage/collections/config",
            urllib.parse.urlencode(url_params).encode("utf-8"),
            method="GET",
            headers={
                "Authorization": _encode_username_password(creds),
            },
        ),
        context=ctx,
    )
    response_json = json.load(response)
    if mode == "full":
        return json.dumps(response_json, indent=2)
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
    return json.dumps(entries, indent=2)


def get_data(creds: str, host: str, addon_name: str, collection: str) -> str:
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{host}/servicesNS/nobody/{addon_name}/storage/collections/"
            f"data/{collection}",
            method="GET",
            headers={
                "Authorization": _encode_username_password(creds),
            },
        ),
        context=ctx,
    )
    response_json = json.load(response)
    return json.dumps(response_json, indent=2)


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument(
        "-a",
        "--addon",
        required=True,
        help="Addon name to get config/data for",
    )
    get_parser.add_argument(
        "-c",
        "--collection",
        default=None,
        required=False,
        help="Collection name to get data from",
    )
    get_parser.add_argument(
        "-u",
        required=True,
        help="Username and password, in `username:password` format",
    )
    get_parser.add_argument(
        "--host",
        default="https://localhost:8089",
        help="Scheme, host and port in `scheme://host:port` format",
    )
    get_parser.add_argument(
        "-m",
        "--mode",
        default="default",
        choices=["default", "full"],
        help="Controls the amount of data printed",
    )
    args = parser.parse_args(argv)
    if args.command == "get":
        if args.collection is None:
            print(get_config(args.u, args.host, args.addon, args.mode))
        else:
            print(get_data(args.u, args.host, args.addon, args.collection))


if __name__ == "__main__":
    main()
