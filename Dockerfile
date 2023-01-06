FROM python:3.10.6 as python_base

FROM python_base as production

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


COPY . /app

EXPOSE 8000

CMD alembic upgrade head && uvicorn src.main:build_app --host 0.0.0.0
