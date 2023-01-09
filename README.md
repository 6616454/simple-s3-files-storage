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
* Aioboto3 (async library for interacting with s3 using python)
* Poetry (Packaging and dependency management);
* PyTest (Framework for tests);

### Project Deployment
1.Clone repository
<!-- TOC -->
    git clone https://github.com/6616454/simple-s3-files-storage.git
2.Copy .env file
<!-- TOC -->
    cp .envexample .env

3.Run the "make up" command
<!-- TOC -->
    make up
4.Wait for the application to launch and, if possible, run the tests
<!-- TOC -->
    docker exec -it fastapi-app sh
    ...
    pytest tests

4. The application is available at
<!-- TOC -->
    0.0.0.0:8082/docs

