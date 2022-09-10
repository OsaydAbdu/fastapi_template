#! /usr/bin/env bash
set -e
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )


cd $root_path

set +x
export POSTGRES_PASSWORD=$(aws --region "us-east-2" ssm get-parameter --name "/vote/osayd.io/postgres/password" --with-decryption --query Parameter.Value | xargs)
export DASHBOARD_PASSWORD="$(aws --region "us-east-2" ssm get-parameter --name "/vote/osayd.io/traefik/password" --with-decryption --query Parameter.Value | xargs)"

set -x
source $root_path/version.sh

docker-compose -f docker-compose.yml -f docker-compose.prod.yml  up -d
