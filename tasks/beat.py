from celery.schedules import crontab
from app.workers.celery_app import celery_app

celery_app.conf.beat_schedule = {
    # Channel 1: 3 videos/week (Mon, Wed, Fri at 10:00)
    'run-trending-pipeline': {
        'task': 'app.workers.trending_pipeline.run_trending_pipeline',
        'schedule': crontab(hour=10, minute=0, day_of_week='1,3,5'),
    },
    # Channel 2: 1 video/week (Sun at 12:00)
    'run-evergreen-pipeline': {
        'task': 'app.workers.evergreen_pipeline.run_evergreen_pipeline',
        'schedule': crontab(hour=12, minute=0, day_of_week='0'),
    },
}
