import os
from datetime import datetime
import subprocess
from flask import send_file

from . import admin

@admin.route("/api/backup/status", methods=["POST"])
def backup_status():
    backup_dir = os.environ.get("BACKUP_PATH")
    newest_time = None
    for f in os.listdir(backup_dir):
        full_path = os.path.join(backup_dir, f)
        if os.path.isfile(full_path):
            try:
                t = datetime.strptime(str(f).strip("n0blog-").strip(".zip"), "%Y%m%d%H%M%S")
                if newest_time == None or t > newest_time:
                    newest_time = t
            except:
                pass
    return newest_time.strftime("%Y-%m-%d %H:%M:%S") if newest_time else "None"

@admin.route("/api/backup/backup", methods=["POST"])
def backup():
    cmd = """rm -f $BACKUP_PATH/* && pg_dump -h sql -d n0blog -U n0blog -f /posts/backup.sql && zip -v -r $BACKUP_PATH/n0blog-`date '+%Y%m%d%H%M%S'`.zip $POSTS_PATH"""
    process = os.popen(cmd, "r")
    result = process.read()
    process.close()
    return result

@admin.route("/api/backup/backup")
def backup_download():
    backup_dir = os.environ.get("BACKUP_PATH")
    newest_time = None
    fn = None
    for f in os.listdir(backup_dir):
        full_path = os.path.join(backup_dir, f)
        if os.path.isfile(full_path):
            try:
                t = datetime.strptime(str(f).strip("n0blog-").strip(".zip"), "%Y%m%d%H%M%S")
                if newest_time == None or t > newest_time:
                    newest_time = t
                    fn = full_path
            except:
                pass
    if fn:
        return send_file(fn)
    else:
        return "No back up file available."
