release: python manage.py migrate
web: gunicorn config.wsgi:application --workers 3 --bind 0.0.0.0:8080
worker: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app beat --loglevel=info
