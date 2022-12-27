FROM python:3.10.6


WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


COPY . /app


CMD sleep 5 && alembic upgrade head && python -m src.main