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

### Register new user
Path: **/users**  
Description: The endpoint is used for a new user creation and registration. After the registration, the user is not activated. A confirmation email is sent by a third party service with an activation code. The user must access the activation link within a minute after the registration.  
Request type: **POST**  
Body type: **JSON**  
Body fields:  
- **email**: string - user email
- **password**: string - user password

Reponses:
- **200: OK** - new user registrated
- **400: Bad Request** - invalid input data or user already registered
- **500: Internal Server Error** - server error

### Activate user
Path: **/activate/{activation_data}**  

Description: The activate endpoint is accessed from the activation email received by the user after registration. The **activation_data** parameter is a base64 string composed of the user uuid (e.g. "7ee13bdb-533a-4822-af81-1d09e3e5800b") and the 4 digit activation code (e.g. "6389") split by ":" character. If the endpoint is accessed within a minute after the user registration with the correct uuid and activation code, then the user is activated.  

Request type: **GET**  

Parameters:
- **activation_data**: string - base64 string encoded from uuid concatenated with activation code (e.g. "uuid:code", 7ee13bdb-533a-4822-af81-1d09e3e5800b:6389)

Reponses:
- **200: OK** - user activated
- **400: Bad Request** - invalid input data or user already activated
- **500: Internal Server Error** - server error



