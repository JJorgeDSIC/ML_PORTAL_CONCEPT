#!/bin/bash
/etc/init.d/rabbitmq-server start
celery -A prhlt2 worker -l info &
python manage.py runserver 0.0.0.0:9000
