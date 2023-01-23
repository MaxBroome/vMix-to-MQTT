FROM python:3.8

RUN pip install requests

RUN pip install paho-mqtt schedule

COPY onair.py /app/main.py

CMD ["python", "/app/main.py"]
