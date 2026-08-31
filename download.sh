#!/bin/bash
set -euo pipefail
set -x

#curl -L -o asndb.gz "https://ipinfo.io/data/ipinfo_lite.json.gz?_src=frontend&token=xxxxxx"

#gunzip -d asndb.gz

#jq -c '{network, asn, as_name}' asndb > asndb-filtered

function make_all_ranges(){
	./export-networks.py -s asndb-filtered -d "$1" -f "$2" --force
}

make_all_ranges ./google "google"
make_all_ranges ./netflix "netflix"
make_all_ranges ./amazon "amazon"
