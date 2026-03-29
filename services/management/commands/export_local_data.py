"""
Export app data from your local DB (e.g. SQLite) for loading on Render/Postgres.

Usage (from project root, with venv active):
  python manage.py export_local_data
  python manage.py export_local_data --output my_backup.json

Then on the live server (Render Shell or SSH):
  python manage.py loaddata my_backup.json

Copy the media/ folder to production so profile images work (see command help).
"""
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Dump all services.* models to a JSON fixture for production import. "
        "Run against your local database that has the data you want to copy."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            default="local_export.json",
            help="Output file path (default: local_export.json in project root)",
        )

    def handle(self, *args, **options):
        out = Path(options["output"])
        if not out.is_absolute():
            from django.conf import settings

            out = Path(settings.BASE_DIR) / out

        self.stdout.write(
            "Exporting services app (users, fundis, bookings, reviews, payments)..."
        )
        with out.open("w", encoding="utf-8") as fh:
            call_command(
                "dumpdata",
                "services",
                natural_foreign=True,
                natural_primary=True,
                indent=2,
                stdout=fh,
            )
        self.stdout.write(self.style.SUCCESS(f"Wrote {out}"))
        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "Security: this file contains password hashes. Do not commit it to git."
            )
        )
        self.stdout.write("")
        self.stdout.write("Next steps for production:")
        self.stdout.write(
            "  A) Automated one-time import (build.sh): "
            "upload local_export.json to private cloud storage, copy a direct-download HTTPS link."
        )
        self.stdout.write(
            "     In Render Dashboard: Web Service - Environment, add (as Secret):"
        )
        self.stdout.write("       RUN_SEED_IMPORT = true")
        self.stdout.write("       SEED_FIXTURE_URL = <that link>")
        self.stdout.write(
            "     Optional: zip your local media/ folder, upload, add MEDIA_ZIP_URL = <zip direct link>"
        )
        self.stdout.write(
            "     Push/deploy once. When the build succeeds, DELETE RUN_SEED_IMPORT "
            "and the URL vars (or set RUN_SEED_IMPORT false) so the next deploy does not re-import."
        )
        self.stdout.write(
            "  B) Manual: Render Shell: upload file, run: python manage.py loaddata local_export.json"
        )
