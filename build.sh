#!/usr/bin/env bash
set -o errexit

# Render runs this before collectstatic; dependencies are not auto-installed for this build command.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# One-time data import (set in Render Dashboard, deploy once, then remove these env vars):
#   RUN_SEED_IMPORT=true
#   SEED_FIXTURE_URL=<private HTTPS URL to local_export.json>  (e.g. Dropbox / Drive direct download)
# Optional profile photos:
#   MEDIA_ZIP_URL=<private HTTPS URL to a zip of your local media/ folder>
if [ "${RUN_SEED_IMPORT:-}" = "true" ] && [ -n "${SEED_FIXTURE_URL:-}" ]; then
  echo "One-time loaddata from SEED_FIXTURE_URL..."
  curl -fsSL "$SEED_FIXTURE_URL" -o /tmp/seed.json
  python manage.py loaddata /tmp/seed.json
  rm -f /tmp/seed.json
fi

if [ "${RUN_SEED_IMPORT:-}" = "true" ] && [ -n "${MEDIA_ZIP_URL:-}" ]; then
  echo "One-time media extract from MEDIA_ZIP_URL..."
  curl -fsSL "$MEDIA_ZIP_URL" -o /tmp/media_seed.zip
  python -c "import zipfile; zipfile.ZipFile('/tmp/media_seed.zip').extractall('.')"
  rm -f /tmp/media_seed.zip
fi

