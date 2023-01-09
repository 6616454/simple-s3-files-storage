## API Simple Storage Files
The API that I created as part of a training project implements 
storage for files
weighing less than 1 GB.

### Used technologies
* Python;
* FastAPI (Web Framework);
* Docker and Docker-Compose (Containerization);
* PostgreSQL (Database);
* Redis (Cache);
* SQLAlchemy (ORM Python);
* Alembic (Database migrations);
* MinIO (S3 Storage);
* Poetry (Packaging and dependency management);
* PyTest (Framework for tests);

### Project Deployment

1. Copy .env file
<!-- TOC -->
    cp .envexample .env

2. Поднять локально Docker-контейнеры
<!-- TOC -->
    make up
3. Войти в контейнер с приложением и запустить тесты
<!-- TOC -->
    docker exec -it fastapi-app sh
    ...
    pytest tests/test_main.py

4. Приложение доступно по адресу
<!-- TOC -->
    0.0.0.0:8082/docs

