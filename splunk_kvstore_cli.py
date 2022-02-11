import argparse
import base64
import json
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://localhost:8089/servicesNS/nobody"


def _encode_username_password(username_password: str) -> str:
    username_password_bytes = username_password.encode("utf-8")
    basic_auth = base64.b64encode(username_password_bytes).strip().decode("utf-8")
    return f"Basic {basic_auth}"


def get_config(username_password: str, app: str, mode: str) -> str:
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{BASE_URL}/{app}/storage/collections/config?output_mode=json",
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


def get_data(username_password: str, app: str, collection: str) -> str:
    response = urllib.request.urlopen(
        urllib.request.Request(
            f"{BASE_URL}/{app}/storage/collections/data/{collection}",
            method="GET",
            headers={
                "Authorization": _encode_username_password(username_password),
            },
        ),
        context=ctx,
    )
    response_json = json.load(response)
    return json.dumps(response_json)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser("config")
    config_parser.add_argument("-u", required=True)
    config_parser.add_argument("-a", "--app", required=True)
    config_parser.add_argument("-m", "--mode", default="default")
    data_parser = subparsers.add_parser("data")
    data_parser.add_argument("-u", required=True)
    data_parser.add_argument("-a", "--app", required=True)
    data_parser.add_argument("-c", "--collection", required=True)
    args = parser.parse_args()
    if args.command == "config":
        print(get_config(args.u, args.app, args.mode))
    elif args.command == "data":
        print(get_data(args.u, args.app, args.collection))


if __name__ == "__main__":
    main()
