# User Registration API

## Description
This repository contains a demo project for a user registration API implemented in Python with Flask, Postgres, and Docker.  
The API supports the following use cases:
- Create an user with an email and a password.
- Send an email to the user with a 4 digits code.
- Activate this account with the 4 digits code received.
- The user has only one minute to use this code. After that, an error should be raised.

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

## Web service project structure
The Flask web service contains the following modules:
- routes.py - Flask endpoints and routes
- models.py - DB related functions and ORM
- email.py - contains EmailAPIController, a class for an external email API communication
- helpers.py - helper functions  

For database upgrade and migrations the project uses Alembic (/migrations folder) and related Flask migration extension. 

The unit and functional tests are located in /web/tests/ folder:
- test_helpers.py - tests for helper functions
- test_api.py - tests for API endpoints
- test_db.py - tests for DB functions 

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


## Running and Testing

### Running the tests on Test environment

Create and start the containers with docker-compoes:  
```
docker-compose -f docker-compose.test.yml up
```

Run the tests with docker-compose command:  
```
docker-compose exec web python manage.py test
```

If the previous command doesn't work, run within the container:
```
docker exec -it <container_id> /bin/bash
root@<container_id>:/usr/src/app# python manage.py test 
```

### Running the Development environment
Create and start the containers with docker-compoes:  
```
docker-compose -f docker-compose.yml up
```

Access the enpoints (e.g. using curl or Postman) on the following paths:

- user registration request - http://127.0.0.1:5000/users
Example curl request:
```
curl --location --request POST 'http://127.0.0.1:5000/users' --header 'Content-Type: application/json' --data-raw '{ "email": "test@email.com", "password": "password" }'
```

- user activation - http://127.0.0.1:5000/activate/{activation_data}

Example curl request:
```
curl --location --request GET 'http://127.0.0.1:5000/activate/NDE3NWU3Y2QtMWI2NS00NTk0LTg3NjItZTI5ODkxNTc1YjJhOjAwNDc%3D'
```
Obs. The activation_data string can be found in the web container Docker logs, like in the following example with:
```
user-api-web-1    |         Hello,
user-api-web-1    |
user-api-web-1    |         Thank you for your registration.
user-api-web-1    |         Please use the following link to complete the registration process and activate your account:
user-api-web-1    |         http://127.0.0.1:5000/activate/NDE3NWU3Y2QtMWI2NS00NTk0LTg3NjItZTI5ODkxNTc1YjJhOjAwNDc%3D
```
The activation email body is printed in the Docker logs containing the activation data base64 string (e.g. "NDE3NWU3Y2QtMWI2NS00NTk0LTg3NjItZTI5ODkxNTc1YjJhOjAwNDc%3D").

### Running the Prod environment
Create and start the containers with docker-compoes:  
```
docker-compose -f docker-compose.prod.yml up
```

Access the enpoints (e.g. using curl or Postman) on the following paths:

- user registration request - http://127.0.0.1:1337/users
Example curl request:
```
curl --location --request POST 'http://127.0.0.1:5000/users' --header 'Content-Type: application/json' --data-raw '{ "email": "test@email.com", "password": "password" }'
```

- user activation - http://127.0.0.1:1337/activate/{activation_data}

Example curl request:
```
curl --location --request GET 'http://127.0.0.1:1337/activate/NDE3NWU3Y2QtMWI2NS00NTk0LTg3NjItZTI5ODkxNTc1YjJhOjAwNDc%3D'
```

## To be improved

- use OpenAPI specification for endpoints, data validation, versions, and documentation. This can be done using connexion or other extensions/frameworks.
- better decoupling and testing for EmailAPIController used for external API integration. Now it uses a mocked/hardcoded implementation for the API request and prints the email body text in the console/logs.
- use authentication using API key, token or other methods.
- instead of Flask framework, **FasAPI** and **uvicorn** can be used. It comes with OpenAPI specification and data validation by default, it is much faster than Flask and it uses async.
