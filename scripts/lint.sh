#!/bin/bash -e

APP_PATH="hatchway"

ruff $APP_PATH

black $APP_PATH --check

isort $APP_PATH --check-only
