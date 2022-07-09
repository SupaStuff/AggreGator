#!/bin/bash

find . -name '__pycache__' | xargs rm -rf
rm -rf \
  poetry.lock \
  .venv/* \
  .coverage \
  .pytest_cache/
