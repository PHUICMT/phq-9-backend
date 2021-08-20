FROM python:3.9

WORKDIR /server

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000
CMD [ "python", "./app/app.py"]