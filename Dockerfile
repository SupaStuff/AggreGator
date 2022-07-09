FROM supastuff/python:poetry as builder

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml .
RUN /home/python/.local/bin/poetry install --no-dev --no-root
COPY . .
RUN poetry build && .venv/bin/pip install dist/*.whl

FROM python:3.10.5-slim as final

COPY --from=builder /app/.venv /opt/venv
COPY exe/* /opt/venv/bin
ENV PATH="/opt/venv/bin:$PATH"
