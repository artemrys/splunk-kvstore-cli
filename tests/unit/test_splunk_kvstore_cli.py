import json

from splunk_kvstore_cli import main


def test_main_when_getting_config_when_full_mode(capsys, mock_urlopen):
    resp = {
        "links": {
            "create": "/servicesNS/nobody/addon_name/storage/collections/config/_new",
            "_reload": "/servicesNS/nobody/addon_name/storage/collections/config/_reload",
            "_acl": "/servicesNS/nobody/addon_name/storage/collections/config/_acl",
        },
        "origin": "https://localhost:8089/servicesNS/nobody/addon_name/storage/collections/config",
        "updated": "2022-12-21T20:45:30+01:00",
        "generator": {"build": "dd0128b1f8cd", "version": "9.0.3"},
        "entry": [
            {
                "name": "addon_name",
                "id": "https://localhost:8089/servicesNS/nobody/addon_name/storage/collections/config/addon_name",
                "updated": "2022-10-14T21:26:21+02:00",
                "links": {
                    "alternate": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name",
                    "list": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name",
                    "_reload": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name/_reload",
                    "edit": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name",
                    "remove": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name",
                    "disable": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name/disable",
                },
                "author": "splunk-system-user",
                "acl": {
                    "app": "addon_name",
                    "can_change_perms": True,
                    "can_list": True,
                    "can_share_app": True,
                    "can_share_global": True,
                    "can_share_user": True,
                    "can_write": True,
                    "modifiable": True,
                    "owner": "splunk-system-user",
                    "perms": {"read": ["*"], "write": ["admin", "sc_admin"]},
                    "removable": True,
                    "sharing": "global",
                },
                "content": {
                    "disabled": False,
                    "eai:acl": None,
                    "eai:appName": "addon_name",
                    "eai:userName": "nobody",
                    "field.state": "string",
                    "profilingEnabled": "False",
                    "profilingThresholdMs": "1000",
                    "replicate": "False",
                    "replication_dump_maximum_file_size": "10240",
                    "replication_dump_strategy": "auto",
                    "type": "undefined",
                },
            }
        ],
        "paging": {"total": 1, "perPage": 30, "offset": 0},
        "messages": [],
    }
    mock_urlopen.return_value.read.return_value = json.dumps(resp).encode()

    main(
        [
            "get",
            "-a",
            "addon_name",
            "-u",
            "user:password",
            "--mode",
            "full",
        ]
    )

    captured = capsys.readouterr()
    expected_result = json.dumps(resp, indent=2) + "\n"

    assert captured.out == expected_result


def test_main_when_getting_config_when_default_mode(capsys, mock_urlopen):
    resp = {
        "links": {
            "create": "/servicesNS/nobody/addon_name/storage/collections/config/_new",
            "_reload": "/servicesNS/nobody/addon_name/storage/collections/config/_reload",
            "_acl": "/servicesNS/nobody/addon_name/storage/collections/config/_acl",
        },
        "origin": "https://localhost:8089/servicesNS/nobody/addon_name/storage/collections/config",
        "updated": "2022-12-21T20:45:30+01:00",
        "generator": {"build": "dd0128b1f8cd", "version": "9.0.3"},
        "entry": [
            {
                "name": "addon_name_collection",
                "id": "https://localhost:8089/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection",
                "updated": "2022-10-14T21:26:21+02:00",
                "links": {
                    "alternate": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection",
                    "list": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection",
                    "_reload": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection/_reload",
                    "edit": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection",
                    "remove": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection",
                    "disable": "/servicesNS/nobody/addon_name/storage/collections/config/addon_name_collection/disable",
                },
                "author": "splunk-system-user",
                "acl": {
                    "app": "addon_name",
                    "can_change_perms": True,
                    "can_list": True,
                    "can_share_app": True,
                    "can_share_global": True,
                    "can_share_user": True,
                    "can_write": True,
                    "modifiable": True,
                    "owner": "splunk-system-user",
                    "perms": {"read": ["*"], "write": ["admin", "sc_admin"]},
                    "removable": True,
                    "sharing": "global",
                },
                "content": {
                    "disabled": False,
                    "eai:acl": None,
                    "eai:appName": "addon_name",
                    "eai:userName": "nobody",
                    "field.state": "string",
                    "profilingEnabled": "False",
                    "profilingThresholdMs": "1000",
                    "replicate": "False",
                    "replication_dump_maximum_file_size": "10240",
                    "replication_dump_strategy": "auto",
                    "type": "undefined",
                },
            }
        ],
        "paging": {"total": 1, "perPage": 30, "offset": 0},
        "messages": [],
    }
    mock_urlopen.return_value.read.return_value = json.dumps(resp).encode()

    main(
        [
            "get",
            "-a",
            "addon_name",
            "-u",
            "user:password",
        ]
    )

    captured = capsys.readouterr()
    expected_result = (
        json.dumps(
            [
                {
                    "name": "addon_name_collection",
                    "updated": "2022-10-14T21:26:21+02:00",
                    "author": "splunk-system-user",
                    "acl": {
                        "app": "addon_name",
                        "can_change_perms": True,
                        "can_list": True,
                        "can_share_app": True,
                        "can_share_global": True,
                        "can_share_user": True,
                        "can_write": True,
                        "modifiable": True,
                        "owner": "splunk-system-user",
                        "perms": {"read": ["*"], "write": ["admin", "sc_admin"]},
                        "removable": True,
                        "sharing": "global",
                    },
                    "content": {
                        "disabled": False,
                        "eai:acl": None,
                        "eai:appName": "addon_name",
                        "eai:userName": "nobody",
                        "field.state": "string",
                        "profilingEnabled": "False",
                        "profilingThresholdMs": "1000",
                        "replicate": "False",
                        "replication_dump_maximum_file_size": "10240",
                        "replication_dump_strategy": "auto",
                        "type": "undefined",
                    },
                }
            ],
            indent=2,
        )
        + "\n"
    )

    assert captured.out == expected_result


def test_main_when_getting_data(capsys, mock_urlopen):
    resp = [{"state": '{"some": "data"}', "_user": "nobody", "_key": "collection_key"}]
    mock_urlopen.return_value.read.return_value = json.dumps(resp).encode()

    main(
        [
            "get",
            "-a",
            "addon_name",
            "-c",
            "addon_name_collection",
            "-u",
            "user:password",
        ]
    )

    captured = capsys.readouterr()
    expected_result = json.dumps(resp, indent=2) + "\n"

    assert captured.out == expected_result
