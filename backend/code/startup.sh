#!/bin/bash
ls venv_for_linux
source ./venv_for_linux/bin/activate
./venv_for_linux/bin/gunicorn -b :5000 server:app
