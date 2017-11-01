# ML_PORTAL_CONCEPT
Machine Learning easy-to-use portal (concept)

### Requirements

* Python 2.7
* Django
* Celery
* Docker (for the container version)

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

* python manage.py runserver 0.0.0.0:8000

Example users (username/pass):

* test / test
* test2 / test2

The first user is the admin user, you can access to the admin site through localhost:8000/admin/ and create new users.

### Docker 

It is included a DockerFile to build and deploy the app, do the following:

* docker build --no-cache -t ml_portal .
* docker run -p 9000:9000 -i -t ml_portal ./run.sh

### TO DO

-Find a lighter initial docker image

