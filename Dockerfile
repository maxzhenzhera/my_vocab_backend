FROM python:3.9.7-slim as base


WORKDIR /my_vocab_backend

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system --deploy

ENV PYTHONPATH=/my_vocab_backend

COPY . .

RUN python ./scripts/make_directories_for_logs.py

CMD ["python", "/my_vocab_backend/app/main.py"]



FROM base as test


RUN pip install pytest pytest-asyncio

CMD ["pytest"]