# User Registration API

## Description
This repository contains a demo project for an user registration API implemented in Python with Flask, Postgres, and Docker.

## Project architecture and environments
### Dev/Test Environment
In the Development or Testing environment there are two Docker containers created with docker-compose:
- web service container
- Postgres DB container

### Prod Environment
In the Production environment there are three Docker containers:
- web service container (with gunicorn)
- Nginx container (proxy)
- Postgres DB container

## Architecture diagram

![alt text](https://github.com/fnastase/user-api/blob/main/image.png?raw=true)

## API Endpoints

### Register new user ```/users```

Path: ```/users```

Request: POST
Type: JSON
Body parameters:
- ```email: string```
- ```password: string```

Reponses:
- 200: OK - new user registrated
- 400: Bad Request - invalid input data or user already registered
- 500: Internal Server Error

