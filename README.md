# splunk-kvstore-cli

This is a small utility that helps to query Splunk KV Store (intended to use with [`jq`](https://stedolan.github.io/jq/)).  

This tool is intended for local development only.

Commands available:

* `kv login -c user:password`
* `kv get addon_name`
* `kv get addon_name:collection_name`
