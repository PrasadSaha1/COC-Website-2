release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn COC_app.wsgi:application
