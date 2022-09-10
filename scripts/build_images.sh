#! /usr/bin/env bash
set -e

set -x
ENV="${2:-remote}"

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )

if [ "$ENV" = "dev" ]; then
	docker-compose build
elif [ "$ENV" = "remote" ]; then
	export TAG="${1}"
	set +x
	export POSTGRES_PASSWORD=$(aws --region "us-east-2" ssm get-parameter --name "/vote/osayd.io/postgres/password" --with-decryption --query Parameter.Value | xargs)
	set -x
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
else
    echo "Wrong first argument" >&2
    echo "Usage: $0 version_numbe [dev|remote]" >&2
    exit 1
fi
