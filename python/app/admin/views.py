from flask import render_template, redirect, request, \
        url_for, flash, session

from . import admin
from .forms import AdminLoginForm

@admin.before_request
def before_request():
    if request.path == url_for('admin.login'):
        return
    if 'login' in session:
        if session['login'] is True:
            if request.path == url_for('admin.login'):
                flash("Already logged in.")
                return redirect(url_for('admin'))
            return
    return redirect(url_for('admin.login'))

@admin.route("/login")
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password == os.getenv("ADMIN_PASS"):
            session['login'] = True
        else:
            return redirect(url_for('admin.login'))
    return render_template("admin_login.html", form=form)

@admin.route("/")
def admin_index():
    return "admin_index"
