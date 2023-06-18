FROM python:3.9-slim

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /backend

# RUN ["python", "manage.py", "json_ingredients_import"]
#
# WORKDIR ..

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "foodgram.wsgi"]
