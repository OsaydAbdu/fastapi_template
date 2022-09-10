#! /usr/bin/env bash

set -e
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )

docker run --rm -v \
	`pwd`/:/home/ python:3.9 bash -c "
		cd /home && \
		curl -sSL https://install.python-poetry.org | \
		python3 - && export PATH=/root/.local/bin:\$PATH && poetry lock -vv\
	"
