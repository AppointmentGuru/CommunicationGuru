# python manage.py migrate
# python manage.py collectstatic --no-input
gunicorn communications.wsgi:application -b :80 --reload
