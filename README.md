# Flask_App-AWS-
Deployment of Two Tier App on AWS

Step By Step Guide :- 
Step 1 :- Update the package by running - sudo apt update

Step 2 :- Install Docker - sudo apt install docker.io

Step 3 :- docker ps

Step 4 :- Give permission to docker ps by running - sudo chown $USER --path of docker ps

Step 5 :- git clone https://github.com/vivekbonde15l/Flask_App-AWS-.git

Step 6 :- go into flask app by - cd {F tab}

Step 7 :- vim Dockerfile 

In Dockerfile write - 
FROM python:3.9-slim

Workdir /app

RUN apt-get update -y\
    && apt-get upgrade -y\
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt  .

RUN pip install mysqlclient
RUN pip install -r requirements.txt

COPY . .

CMD ["python","app.py"]

Step 8 :- docker build . -t flaskapp

Step 9 :- docker run -d -p 8080:8080 flaskapp:latest  (Create a docker image of flaskapp)

Step 10 :- docker login 
Username :- vivekbonde15l
Password :- 

Step 11:- docker tag flaskapp:latest vivekbonde2003 /flaskapp:latest

Step 12 :- docker images

Step 13 :- docker push vivekbonde2003/flaskapp:latest

Step 14 :- sudo apt install docker-compose

Step 15 :- vim docker-compose.yml 

Write in File :- Yet Another Markup Language

version: '3'
services:
   backend:
    image : vivekbonde2003/flaskapp:latest
    ports:
      - "8080:8080"
    environment:
      MYSQL_HOST: "mysql"
      MYSQL_USER: "admin"
      MYSQL_PASSWORD: "admin"
      MYSQL_DB: "myDb"
    depends_on:
      - mysql

  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: "root"
      MYSQL_DATABASE: "myDb"
      MYSQL_USER: "admin"
      MYSQL_PASSWORD: "admin"
    ports :
        - "3306:3306"
    volumes:
      - ./message.sql:/docker-entrypoint-initdb.d/message.sql   # Mount sql script into container's /docker-entrypoint-initdb.d directory to get table automatically created
      - mysql-data:/var/lib/mysql  # Mount the volume for MySQL data storage

volumes:
  mysql-data:

Step 16 :- docker-compose up -d 