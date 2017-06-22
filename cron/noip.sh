#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/../config/env.sh

echo $NOIP_USER
echo $NOIP_PW

PI_IP=`hostname -I`

echo $PI_IP

URL="https://${NOIP_USER}:${NOIP_PW}@dynupdate.no-ip.com/nic/update?hostname=venusaur.ddns.net&myip=${PI_IP}"
echo $URL

curl -v "$URL"
#curl -v https://www.duckdns.org/update?domains=venusaur&token=36396274-9076-4db8-9ebe-6c07a3483da6&ip=10.75.0.199&verbose=true
