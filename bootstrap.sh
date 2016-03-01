#! /bin/bash
[ ! -d venv ] && virtualenv venv
./venv/bin/pip install -r requirements.txt
