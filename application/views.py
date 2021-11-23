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

if __name__ == '_@views__':
    views.run()

@views.route('/')
def index():
    return render_template('homePage.html')

@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('homePage.html', name=current_user.name.capitalize(),
                               type=current_user.type.capitalize())
    return render_template("homePage.html")

@views.route('/employee', methods=["GET", "POST"])
@login_required
def loggedIn():
    return render_template("homePage.html", name=current_user.name.capitalize(),
                           type=current_user.type.capitalize())

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

@views.route('/NewCustomerForm', methods=["GET", "POST"])
def newCustomer():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        passW = request.form.get("passW")
        email = request.form.get("email")
        phoneNum = request.form.get("phoneNum")
        cust_address = request.form.get("cust_address")

        #if user already exists, redirect back to signup form
        user1 = User.query.filter_by(email=email).first()
        if user1:
            flash('Email address already exists')
            return redirect(url_for('views.NewCustomerForm'))

        new_user = User(email = email, name = fname,
                        password = generate_password_hash(passW, method='sha256'))

        try:
            with connect(
                host = host,
                user = user,
                password = password,
                database = database
            ) as connection:
                print(connection)

                # ADD SEQUEL SHIT
                insert_customer = "" #do dis
                query = "" #do dis

                with connection.cursor(buffered=True) as cursor:
                    #cursor.execute(insert_customer)
                    #connection.commit()
                    cursor.execute(query)
                    temp = cursor.fetchone()
                    print("Successfully inputted data into DB")

                    if temp is not None:
                        flash('Email already exists')
                        return redirect(url_for('views.NewCustomerForm'))
                    else:
                        cursor.execute(insert_customer)
                        connection.commit()
                        cursor.execute(query)
                        temp = cursor.fetchone()

                        db.session.add(new_user)
                        db.session.commit()

                        custInfo = {
                            "fname": fname,
                            "lname": lname,
                            "email": email,
                            "phoneNum": phoneNum,
                            "cust_address": cust_address
                        }
                        return render_template("CustomerConfirmation.html")
        except Error as e:
            print(e)
    return render_template("NewCustomerForm.html")

@views.route('/Submitted', methods=["GET", "POST"])
def confirmationPage():
    return render_template("ConfirmationPage.html")



