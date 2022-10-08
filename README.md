# Social Network API

Small project demonstrating basic version of social network backend

## Launching

Use docker-compose command to launch project

```bash
docker-compose up --build
```
Service is gonna be available by host 0.0.0.0:8000

## Documentation

You can see all available endpoints requesting api/swagger endpoint
in browser

## Admin panel

In order to see all objects you can enter admin panel through admin/ endpoint

```python
# enter docker container
docker exec -it social_network_api_api_1 bash

# create admin user
python manage.py createsuperuser
```

## Libraries

Used libraries:
1. Djoser for auth
2. Drf-yasg for docs
3. Other smaller libraries for making developing faster 