#! /bin/bash

set -e

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTPATH/../prometheus
docker-compose down
docker volume rm prometheus_prometheus-data
docker-compose up