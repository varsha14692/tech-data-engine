FROM python:3.9-slim-buster
RUN apt update && apt install -y wait-for-it

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ .

CMD [ "wait-for-it", "database:5432", "--", "python3", "main.py"]
