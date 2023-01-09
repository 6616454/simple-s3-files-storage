FROM python:3.10.6 as production

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --upgrade pip

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev


COPY . /app

EXPOSE 8000

CMD sleep 10 && alembic -c ./deploy/alembic.ini upgrade head && python -m src.main
