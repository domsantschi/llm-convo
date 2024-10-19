FROM python:3.9-alpine

WORKDIR /app

# Copy the application files
COPY app.py /app/
COPY templates /app/templates

RUN pip install --no-cache-dir Flask requests

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
