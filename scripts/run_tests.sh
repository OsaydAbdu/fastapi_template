#! /usr/bin/env bash
set -e
ENV="${1:-dev}"
OKTA_PROFILE=ease-access-account
export ECR_PYTHON=947865815790.dkr.ecr.eu-central-1.amazonaws.com/mozn_python/python
export PYTHON_TAG=v3.9.13
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )
cd "$root_path"
source $parent_path/poetry_login_creditials.sh $ENV
set -x

export TAG=test
if [ "$ENV" = "dev" ]; then
	docker_compose_cmd="aws-okta exec $OKTA_PROFILE -- docker-compose -f docker-compose.base.yml -f docker-compose.dev.yml "
elif [ "$ENV" = "remote" ]; then
	docker_compose_cmd="docker-compose -f docker-compose.base.yml -f docker-compose.prod.yml "
	pip install 'dvc[s3]'~=2.9.3
	dvc pull
fi
if [ "$2" = "build" ]; then
	# Remove possibly previous broken stacks left hanging after an error
	$docker_compose_cmd down --volumes --timeout 30 --remove-orphans
	$docker_compose_cmd build --parallel
fi
$docker_compose_cmd up -d

if [ "$ENV" = "remote" ]; then
	$docker_compose_cmd exec -T backend pip install pytest pytest-cov
fi
$docker_compose_cmd exec backend python /backend/scripts/wait_for_elastic_search.py
$docker_compose_cmd exec backend python /backend/scripts/wait_for_db.py

$docker_compose_cmd exec backend pytest--cov=app/ --cov-report=term-missing -vv --color=yes tests/
