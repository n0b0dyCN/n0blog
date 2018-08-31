#!/bin/sh

source venv/bin/activate

flask db init
flask db migrate
flask db upgrade

exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - n0blog:app
