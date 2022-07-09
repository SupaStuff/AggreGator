#!/bin/bash

poetry run pytest --cov --cov-report term:skip-covered "$@"
