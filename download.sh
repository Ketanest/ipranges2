#!/bin/bash
set -euo pipefail
set -x

curl -L -o asndb.gz "https://ipinfo.io/data/ipinfo_lite.json.gz?_src=frontend&token=$1"

gunzip -d asndb.gz

jq -c '{network, asn, as_name, as_domain}' asndb > asndb-filtered

function make_all_ranges(){
	./export-networks.py -s asndb-filtered -d "$1" -f "$2" --force
}

make_all_ranges ./google "google"
make_all_ranges ./netflix "netflix"
make_all_ranges ./amazon "amazon"
make_all_ranges ./cloudflare "cloudflare"
make_all_ranges ./facebook "facebook"
make_all_ranges ./apple "apple inc"
make_all_ranges ./github "github"
make_all_ranges ./linode "linode"
make_all_ranges ./microsoft "microsoft"
make_all_ranges ./openai "openai"
make_all_ranges ./oracle "oracle"
make_all_ranges ./telegram "telegram"
make_all_ranges ./vultr "vultr"
make_all_ranges ./twitter "twitter"
make_all_ranges ./proton "proton"
