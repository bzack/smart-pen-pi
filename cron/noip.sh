#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/../config/env.sh

echo $NOIP_USER
echo $NOIP_PW

PI_IP=`hostname -I | sed -e 's/ .*//g'`

echo $PI_IP

#URL="https://${NOIP_USER}:${NOIP_PW}@dynupdate.no-ip.com/nic/update?hostname=venusaur.ddns.net&myip=${PI_IP}"
URL="https://www.duckdns.org/update?domains=smart-pen&token=${DUCK_TOKEN}&ip=${PI_IP}&verbose=true"
#URL="https://www.duckdns.org/update?domains=venusaur&token=${DUCK_TOKEN}&ip=${PI_IP}&verbose=true"
echo $URL

curl -v "$URL"
