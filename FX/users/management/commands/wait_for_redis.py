"""
Django command to wait for database to be available.
"""

import os
import time

import redis
from django.core.management.base import BaseCommand

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DATABASE = os.getenv("REDIS_DATABASE")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


class Command(BaseCommand):
    """Django command to wait for redis."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for redis...")
        redis_up = False
        while redis_up is False:
            try:
                redis_instance = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=REDIS_DATABASE,
                    password=REDIS_PASSWORD,
                )
                redis_instance.get("TEST")
                redis_up = True
            except Exception as e:
                self.stdout.write("redis unavailable, waiting 1 second...")
                self.stdout.write(e)
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("redis available!"))
