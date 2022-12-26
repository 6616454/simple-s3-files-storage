FROM python:3.11

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait


WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN chmod +x /wait


COPY async-python-sprint-4 /app


CMD /wait && alembic upgrade head && python -m src.main