# splunk-kvstore-cli

This is a small utility that helps to query Splunk KV Store (intended to use with [`jq`](https://stedolan.github.io/jq/)).  

This tool is intended for local development, when developing something for Splunk which interacts with KVStore.

## Installation

`pip install splunk-kvstore-cli`

## Examples

> All the examples below can be suffixed with `| jq .` for better output

All the examples below use default value of `--host` parameter which is `https://localhost:8089`, but you can provide your own.

* `kv get -a addon_name -u user:password` - prints data about all the collections associated with the add-on `addon_name`
* `kv get -a addon_name -u user:password -m full` - prints **ALL** data about all the collections associated with the add-on `addon_name`
* `kv get -a addon_name -c collection_name -u user:password` - prints data from the particular collection `collection_name`

### Disclaimer

This is not an official Splunk product.
