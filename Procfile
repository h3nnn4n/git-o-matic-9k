release: python manage.py migrate
web: gunicorn git_o_matic_9k.wsgi --log-file -
main_worker: celery -A git_o_matic_9k worker --beat --loglevel INFO
