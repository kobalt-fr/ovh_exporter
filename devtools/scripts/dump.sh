#! /bin/bash
# Connexion kube pour le dump
# Docker prometheus démarré

set -e

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# EPOCH milliseconds
# 25 mai
start="1716641355000"
# 12 juin
stop="1718196555000"
data="$SCRIPTPATH/../temp/data.dump.gz"

if [ ! -f "$data" ]; then
  date
  echo Dump des données
  kubectl -n prometheus exec statefulsets/prometheus-kube-prometheus-stack-prometheus -- \
    promtool tsdb dump-openmetrics \
      --min-time $start \
      --max-time $stop \
      --match "{job='ovh-exporter',kobalt_client='infrastructure',region=~'(GRA|SBG).*'}" \
      /prometheus/ | gzip > "$data"
  ls -alh "$data"
  date
else
  echo Réutilisation du dump existant
  ls -alh "$data"
fi

date
echo Copie des données
docker exec -u=root -ti prometheus rm -f /tmp/data.dump /tmp/data.dump.gz
docker cp "$data" prometheus:/tmp/data.dump.gz
date
echo Injection des données
docker exec -ti prometheus gunzip -k /tmp/data.dump.gz
docker exec -ti prometheus promtool tsdb create-blocks-from openmetrics /tmp/data.dump /prometheus/data
date
