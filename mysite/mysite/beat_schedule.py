from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check_scheduled_reports': {
        'task': 'mysite.mysite.tasks.check_scheduled_reports',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
    'enforce_data_retention_policies': {
        'task': 'apps.security_app.tasks.enforce_data_retention_policies',
        'schedule': crontab(minute=0, hour=2),  # Run daily at 2 AM
    },
}
