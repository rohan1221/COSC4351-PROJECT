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
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        phNum = request.form.get("phoneNum")
        address = request.form.get("address")
        partySz = request.form.get("party_size")
        date = request.form.get("booking_date")

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                print(connection)

                insert_customer = "INSERT INTO Users (first_name, last_name, email, phone_no, address)" \
                                 "VALUES" \
                                 "('"+ fname + "','"+ lname +"','"+ email +"','"+ phNum +"','"+ address +"')"

                insert_bookings = "INSERT INTO Bookings(firstName, lastName, booking_date, num_guest)" \
                                  "VALUES" \
                                  "('"+ fname +"','"+ lname +"', '"+ date +"', '"+ partySz +"')"

                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(insert_customer)
                    cursor.execute(insert_bookings)
                    connection.commit()

                    getResID = "SELECT Bookings.booking_ID FROM Bookings "\
                               "WHERE booking_date = '"+ date +"' AND num_guest= '"+ partySz +"' AND lastName = "+ lname + ";"
                    cursor.execute(getResID)
                    print("Getting booking ID")
                    resIDresults = cursor.fetchone()
                    print(resIDresults)
                    print("successfully inserted data into DB")

                    resInfo = {
                        "booking_ID": resIDresults[0],
                        "fname": fname,
                        "email": email,
                        "phNum": phNum,
                        "partySz": partySz,
                        "date": date
                    }
        except Error as e:
            print(e)

        return render_template("ConfirmationPage.html", info=resInfo)





