# from __future__ import absolute_import
# import os
# from celery import Celery
# from real_estate.settings import base

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate.settings.development")

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate.settings.development")

# app = Celery("real_estate")

# app.config_from_object("django.conf:settings", namespace="CELERY")


# # Load task modules from all registered Django app configs.

# app.autodiscover_tasks(lambda: base.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")


import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate.settings.development")
# Tell Celery to retry connecting to the broker on startup
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
broker_connection_retry_on_startup = True
app = Celery("real_estate", broker="redis://redis:6379/0")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
