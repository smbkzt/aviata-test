# Aviata-test

## Prerequisites
```
* python == 3.7
* django == 2.1.5
* Celery >= 3.2
```

## Installing
```
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use
```
Run celery: celery -A aviata worker -l info
Run rabbitmq: sudo service rabbitmq-server start
Run app: python manage.py runserver
```

## Endpoints

### List of available directions
```
http://127.0.0.1:8000/directions/
```

### Specific direction
```
http://127.0.0.1:8000/directions/MOW-TSE/
```
