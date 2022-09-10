#! /usr/bin/env bash

# Exit in case of error
set -e
set -x

# Remove all unused images and images that are not used by
#  existing containers that were created before the last 24 hours
docker image prune -a --filter "until=24h" --force

# Remove all stopped containers that were not removed when stopped
docker container prune --filter "until=24h" --force
