from flask import render_template, request
from app import application
from .models import *  

@application.route("/")
def home():
    return render_template("index.html")

@application.route("/login", methods=["GET", "POST"])
def signin():
    print("Login route accessed:", request.method)  

    if request.method == "POST":
        uname = request.form.get("User_name")
        pwd = request.form.get("Password")

        print("Login attempt:", uname, pwd)  

        # Query only by email first to isolate user existence
        usr = User_info.query.filter_by(email=uname).first()
        print("User from DB:", usr)

        if usr:
            print("Password from DB:", usr.password)
            print("Password match:", usr.password == pwd)
            print("Role from DB:", usr.role)
            print("Role match:", usr.role == 0)

            if usr.password == pwd and usr.role == 0:
                print("Redirecting to admin dashboard")
                return render_template("admin_dashboard.html")

        print("Login failed: invalid credentials or role mismatch")

    print("Rendering login page again")  
    return render_template("login.html")

@application.route("/register")
def signup():
    return render_template("signup.html")

@application.route("/fix_admin")
def fix_admin():
    # Delete existing admin
    User_info.query.filter_by(id=1).delete()
    db.session.commit()
    
    # Create fresh admin with clean data
    admin = User_info(
        name="Admin",
        email="admin@ds.iitm.ac.in",
        password="admin@123",
        role=0,
        full_name="Atul Pandey",
        address="IIT Madras",
        pin_code=600036
    )
    
    db.session.add(admin)
    db.session.commit()
    
    # Verify
    check = User_info.query.filter_by(email="admin@ds.iitm.ac.in").first()
    if check:
        return f"Success! Admin recreated. Email: {check.email}, Role: {check.role}"
    else:
        return "Failed to create admin"
