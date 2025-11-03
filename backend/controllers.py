from flask import render_template, request, url_for, redirect
from app import application, db
from .models import User_info, theatre, Shows  
from datetime import datetime

# Home page
@application.route("/")
def home():
    return render_template("index.html")

# Login page and authentication
@application.route("/login", methods=["GET", "POST"])
def signin():
    print("Login route accessed:", request.method)

    if request.method == "POST":
        uname = request.form.get("User_name")
        pwd = request.form.get("Password")
        print("Login attempt:", uname, pwd)

        user = User_info.query.filter_by(email=uname).first()
        print("User from DB:", user)

        if user and user.password == pwd:
            if user.role == 0:
                print("Admin login successful")
                return redirect(url_for("admin_dashboard", name=uname))
            elif user.role == 1:
                print("User login successful")
                return redirect(url_for("user_dashboard", name=uname))
        else:
            print("Invalid login credentials")
            return render_template("login.html", msg="INVALID USER CREDENTIALS")

    return render_template("login.html")

# Registration page and user creation
@application.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        fullname = request.form.get("full_name")
        address = request.form.get("location")
        pin = request.form.get("pin_code")

        user = User_info.query.filter_by(email=uname).first()
        if user:
            print("User already exists:", uname)
            msg = "SORRY, USER ALREADY EXISTS."
            print("Message being sent to template:", msg)
            return render_template("signup.html", msg=msg)

        print("Form data received:", uname, pwd, fullname, address, pin)

        try:
            new_user = User_info(
                email=uname,
                password=pwd,
                full_name=fullname,
                address=address,
                pin_code=pin,
                role=1  # Regular user
            )
            db.session.add(new_user)
            db.session.commit()
            print("User registered successfully:", uname)
            return render_template("login.html", msg="THANK YOU FOR REGISTERING. PLEASE LOGIN.")
        except Exception as e:
            print("Error during registration:", e)
            return f"Registration failed: {e}", 500

    return render_template("signup.html", msg="")

# Common route for admin and user dashboard
@application.route("/admin/<name>")
def admin_dashboard(name):
    theatres = get_theatres()
    return render_template("admin_dashboard.html", name=name, theatres=theatres)

@application.route("/user/<name>")
def user_dashboard(name):
    return render_template("user_dashboard.html", name=name)

@application.route("/venue/<name>", methods=["GET", "POST"])
def add_venue(name):
    if request.method == "POST":
        venue_name = request.form.get("name")
        location = request.form.get("location")
        pin_code = request.form.get("pin_code")
        capacity = request.form.get("capacity")
        new_theatre = theatre(name=venue_name, location=location, pin_code=pin_code, capacity=capacity)
        db.session.add(new_theatre)
        db.session.commit()

        print("Venue submitted:", venue_name, location, pin_code, capacity)

        return redirect(url_for("admin_dashboard", name=name))

    return render_template("add_venue.html", name=name)

@application.route("/show/<venue_id>/<name>", methods=["GET", "POST"])
def add_show(venue_id, name):
    if request.method == "POST":
        s_name = request.form.get("name")
        genre = request.form.get("genre")
        ticket_price = request.form.get("ticket_price")
        date_time = request.form.get("date_time")

        try:
            # Fix datetime format
            dt_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
            new_show = Shows(
                name=s_name,
                genre=genre,
                ticket_price=ticket_price,
                date_time=dt_time,
                theatre_id=venue_id
            )
            db.session.add(new_show) 
            db.session.commit()
            print("Show submitted:", s_name, genre, ticket_price, date_time)
            return redirect(url_for("admin_dashboard", name=name))
        except Exception as e:
            print("Error adding show:", e)
            return render_template("add_show.html", venue_id=venue_id, name=name, msg="Error adding show")

    return render_template("add_show.html", venue_id=venue_id, name=name)

# Other supported function
def get_theatres():
    theatres = theatre.query.all()
    return theatres