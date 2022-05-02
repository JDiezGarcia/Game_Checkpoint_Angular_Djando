#!/bin/bash
set -euo pipefail

find ../backend/game_checkpoint -type d -name migrations -exec find {} -type f ! -name '*NODEL*' ! -name '__init__.py' -delete -print \;
docker exec -itu "$UID" gc_django python manage.py makemigrations users
docker-compose down -t 1
