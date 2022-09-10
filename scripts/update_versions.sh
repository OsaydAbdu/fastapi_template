#! /usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e
# Print every command before running it.
set -x
# This script updates `CHANGELOG.md` and update version in pyproject.toml
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )
cd "$root_path"


export NEW_VERSION=$1
export VERSION_NUMBER=${NEW_VERSION:1}

if [ "$(uname)" == "Darwin" ]; then
    # NOTE: On MacOS which uses BSD sed (instead of GNU sed) you need to specify the backup extension (e.g. ".old")
    sed -i .old 's/^version = \".*\"$/version = \"'$VERSION_NUMBER'\"/' $root_path/backend/pyproject.toml
    sed -i .old 's/^    VERSION: str = ".*\"$/    VERSION: str = \"'$VERSION_NUMBER'\"/' $root_path/backend/app/core/config.py
    rm $root_path/backend/pyproject.toml.old
    rm $root_path/backend/app/core/config.py.old
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sed -i 's/^version = \".*\"$/version = \"'$VERSION_NUMBER'\"/' $root_path/backend/pyproject.toml
    sed -i 's/^VERSION: str = ".*\"$/VERSION: str = \"'$VERSION_NUMBER'\"/' $root_path/backend/app/core/config.py
else
    echo "Unsupported Platform $(uname)"
    exit 1
fi
echo "export TAG=$NEW_VERSION" > $root_path/version.sh

# $root_path/frontend/package.json is not added because it's in a submodule
# Once the code fuly moves here, it'll need to be added.
git add $root_path/backend/pyproject.toml $root_path/backend/app/core/config.py $root_path/version.sh
