#!/bin/bash
set -euo pipefail
set -x

curl -L -o asndb.gz "https://ipinfo.io/data/ipinfo_lite.json.gz?_src=frontend&token=$1"

gunzip -d asndb.gz

jq -c '{network, asn, as_name, as_domain}' asndb > asndb-filtered

function make_all_ranges(){
	./export-networks.py -s asndb-filtered -d "$1" -f "$2" --force
}

declare -A asns=(
	[google]="google"
	[netflix]="netflix"
	[amazon]="amazon"
	[cloudflare]="cloudflare"
	[facebook]="facebook"
	[apple]="apple inc"
	[github]="github"
	[linode]="linode"
	[microsoft]="microsoft"
	[openai]="openai"
	[oracle]="oracle"
	[telegram]="telegram"
	[vultr]="vultr"
	[twitter]="twitter"
	[proton]="proton"
)

for asn in "${!asns[@]}"; do
    make_all_ranges "./$asn" "${asns[$asn]}"
done
