FROM python:3.14.0b2-alpine3.22

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev postgresql-dev

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["python3", "main.py"]