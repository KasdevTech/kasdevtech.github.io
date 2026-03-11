from __future__ import annotations

import argparse

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from .config import load_settings
from .pipeline import run_once


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Blog Generation Agent")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("run-once", help="Run one publishing cycle now")
    sub.add_parser("schedule", help="Run daily scheduler")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    settings = load_settings()

    if args.command == "run-once":
        run_once(settings)
        return

    if args.command == "schedule":
        timezone = pytz.timezone(settings.timezone)
        scheduler = BlockingScheduler(timezone=timezone)
        trigger = CronTrigger(hour=settings.run_hour_24, minute=settings.run_minute, timezone=timezone)

        scheduler.add_job(lambda: run_once(settings), trigger=trigger, max_instances=1, coalesce=True)
        print(
            f"Scheduler started. Will publish {settings.posts_per_run} posts daily at "
            f"{settings.run_hour_24:02d}:{settings.run_minute:02d} {settings.timezone}."
        )
        scheduler.start()
        return

    parser.error("Unknown command")


if __name__ == "__main__":
    main()
