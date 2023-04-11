FROM python:3.11

WORKDIR /app
COPY . /app

MAINTAINER name Chet LUO

RUN pip install -r requirements.txt

CMD ["python","chatbot.py"]
