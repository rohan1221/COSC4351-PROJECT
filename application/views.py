from flask import Flask, request, render_template, redirect, url_for, request, Blueprint, flash, current_app
from mysql.connector import connect, Error
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from . import db
from .models import User, login_required_test
import datetime

views = Blueprint('views', __name__)

host = "localhost"
user = "root"
password = "coogshouse"
database = "group_8"

@views.route('/NewReservation', methods=["GET","POST"])
def newReservation():
    if request.method == "POST":
        send_fname = request.form.get("fname")