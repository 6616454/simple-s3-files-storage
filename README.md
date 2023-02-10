## API Simple Storage Files
API, which is being developed as part of a test task.

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
* JWT (Auth);

### Project Deployment
1.Clone repository
<!-- TOC -->
    git clone https://github.com/6616454/test-task-the-restaurant-menu.git
2.Copy .env file
<!-- TOC -->
    cp .envexample .env

3.Run the "make up" command
<!-- TOC -->
    make up

4. The application is available at
<!-- TOC -->
    127.0.0.1:8000/docs

