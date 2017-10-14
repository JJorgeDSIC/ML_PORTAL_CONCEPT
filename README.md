# ML_PORTAL_CONCEPT
Machine Learning easy-to-use portal (concept)

### Requirements

* Python 2.7
* Django
* Celery

### Installation

* pip install -r requeriments.txt

### For Celery

* sudo apt-get install -y erlang
* sudo apt-get install rabbitmq-server
* celery -A prhlt2 worker -l info

### For running

On ml_portal/

For running Celery:

* celery -A prhlt2 worker -l info

For running django:

* python manage.py runserver

Example users (username/passwors):

* test / test
* test2 / test2

The first user is the admin user, you can access to the admin site through localhost:8000/admin/ and create new users.

