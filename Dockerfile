FROM supastuff/python:poetry as builder

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml .
# There has to be a better way...
RUN mkdir -p src/libs/db/src/aggregator src/apps/cli/src/aggregator \
 && touch src/libs/db/src/aggregator/__init__.py src/apps/cli/src/aggregator/__init__.py
COPY src/libs/db/pyproject.toml src/libs/db/
COPY src/apps/cli/pyproject.toml src/apps/cli/

RUN /home/python/.local/bin/poetry install --no-dev
# Definitely has to be a better way...
RUN rm src/libs/db/src/aggregator/__init__.py src/apps/cli/src/aggregator/__init__.py
# COPY . .
# RUN /home/python/.local/bin/poetry build && .venv/bin/pip install dist/*.whl
COPY src src
RUN find src -name '__pycache__' | xargs rm -rf

FROM python:3.10.5-slim as final

COPY --from=builder /app /opt/aggregator
COPY exe/* /opt/aggregator/.venv/bin
ENV PATH="/opt/aggregator/.venv/bin:$PATH"
