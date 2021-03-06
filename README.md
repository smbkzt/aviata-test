# Aviata-test

## Prerequisites
```
* python == 3.6
* django >= 2
* Celery >= 3.2
* Redis
* RabbitMQ
```

## Installing
```
virtualenv --python=python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use
```
Run celery: celery -A aviata worker -l info
Run celery-beat: celery beat -A aviata -l info
Run rabbitmq: sudo service rabbitmq-server start
Populate data: python manage.py initialize
Run app: python manage.py runserver
```

## Endpoints

### List of available directions
```
http://139.180.192.188/directions/
```

### Specific direction
```
http://139.180.192.188/directions/ALA-TSE/
```
