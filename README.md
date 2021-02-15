# FastAPI App
This is a simple web server application using FastAPI.

[FastAPI](https://fastapi.tiangolo.com/) is a fast, easy to use, robust web micro-framework for building APIs with Python 3.6+.
It makes documentation much easier since it can integrate
your APIs with OpenAPI schemas. It doesn't require you to use a SQL (relational) or NoSQL database, yet, you can use both if needed. In general is great for microservices where you don't need all the batteries that other frameworks, like Django Rest Framework, have which allows your application to be lighter.

## Requirements
- Docker version 20.10.2, build 2291f61

## Instalation and Running

1. Clone this project:
    ```
    git clone https://github.com/cesnietor/fastapi-app.git
    ````

2. The project contains a dockerfile, to build and run the project locally run the following command where you cloned the project:

    ```
    docker-compose up
    ```

    This should create a docker container and start the application on http://localhost:8081

## APIs

FastAPI allows you to see the APIs documented using Swagger at http://localhost:8081/docs

## Tests

This project includes unit tests which can be run inside the docker container.

```
docker exec -it web_app pytest -v
```