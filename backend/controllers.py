from flask import render_template, request
from app import application, db
from .models import User_info

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
                return render_template("admin_dashboard.html")
            elif user.role == 1:
                print("User login successful")
                return render_template("user_dashboard.html")
        else:
            print("Invalid login credentials")
            return render_template("login.html", msg="INVALID USER CREDENTIALS")

    return render_template("login.html", msg="")

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

# Debug route to list all users
@application.route("/debug_users")
def debug_users():
    users = User_info.query.all()
    return "<br>".join([
        f"{u.id} - {u.email} - Role: {u.role} - Name: {u.full_name} - Address: {u.address} - Pin: {u.pin_code}"
        for u in users
    ])