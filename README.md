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

## Populate data
```
python manage.py initialize
```

## Use
```
Run celery: celery -A aviata worker -l info
Run celery-beat: celery beat -A aviata -l info
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
