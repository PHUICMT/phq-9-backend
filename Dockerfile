FROM python:3.9

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./app/app.py"]