#!/usr/bin/env bash

set -e
set -x
export PYTHONPATH=.
python scripts/wait_for_db.py
alembic -c /backend/database/db_alembic/alembic.ini upgrade head
python scripts/init_db.py
if [ "$ENV" = "production" ]; then
	bash -c "gunicorn -w ${NUM_WORKERS} -k uvicorn.workers.UvicornWorker \
	--bind 0.0.0.0:${BACKEND_PORT} --keep-alive 5 --log-level ${BACKEND_LOG_LEVEL} \
	app.main:app"
elif [ "$ENV" = "development" ]; then
    bash -c "uvicorn --reload --proxy-headers --host 0.0.0.0 \
    --port ${BACKEND_PORT}  --log-level ${BACKEND_LOG_LEVEL} \
    app.main:app"
elif [ "$ENV" = "test" ]; then
    bash -c "pytest --cov=app/ --cov-report=term-missing -vv --color=yes tests/ "
elif [ "$ENV" = "ptw" ]; then
    bash -c "ptw app/ tests/ -- --cov=app/ --cov-report=term-missing -vv --color=yes tests/ "
fi
