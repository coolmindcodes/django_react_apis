FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requrements.txt
COPY . /app
CMD python manage.py runserver 0.0.0.0:8000