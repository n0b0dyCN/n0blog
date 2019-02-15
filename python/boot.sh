#!/bin/sh


source venv/bin/activate

sleep 4

flask db init
flask db migrate
flask db upgrade

FILE=$POSTS_PATH/backup.sql
if [ -f $FILE ]; then
    psql -h sql -d n0blog -f $FILE -U n0blog 2&>1 > /dev/null
fi

exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - n0blog:app
