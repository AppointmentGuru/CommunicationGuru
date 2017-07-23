python manage.py migrate
python manage.py collectstatic --no-input
gunicorn communicationguru.wsgi:application -b :80 --reload
