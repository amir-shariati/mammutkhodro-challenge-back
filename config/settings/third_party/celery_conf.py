# import os
# from celery.schedules import crontab
#
# # Celery Configuration Options
# CELERY_TIMEZONE = 'Asia/Tehran'
# # CELERY_TASK_TRACK_STARTED = True
# # CELERY_TASK_TIME_LIMIT = 30 * 60
#
#
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://127.0.0.1:6379/1')
#
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://127.0.0.1:6379/1')
#
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
#
#
# CELERY_BEAT_SCHEDULE = {
#     "weather_update_every_two_hours": {
#         "task": "apps.shipment_app.tasks.weather_update_every_two_hours",
#         "schedule": crontab(minute=0, hour='*/2'),
#     },
# }
