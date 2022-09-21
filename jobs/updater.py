from django.conf.global_settings import TIME_ZONE
from .jobs import Schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


def start():
    print("batch start")
    scheduler = BackgroundScheduler(timezone=pytz.timezone(TIME_ZONE))
    scheduler.add_job(execute_schedule, CronTrigger.from_crontab('0 4 * * *'))
    scheduler.start()


def execute_schedule():
    custom_schedule = Schedule(initial=False)
    return custom_schedule.run()

