FROM python:3.9.4


WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app
CMD python manage.py migrate --no-input && gunicorn -b 0.0.0.0:8000 --log-level info --reload -w 9 project.wsgi:application
