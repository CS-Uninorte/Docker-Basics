FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV DB_HOST=mongodb
ENV DB_PORT=27017

CMD [ "fastapi", "dev", "src/main.py", "--port", "5000", "--host", "0.0.0.0", "--reload" ]
