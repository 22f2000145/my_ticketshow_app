from flask import Flask, render_template
from flask_migrate import Migrate  
from backend.models import db, User_info  
application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticketshow.sqlite3"
 
application.debug = True

db.init_app(application)


# Role fix: ensure admin user has correct integer role
with application.app_context():
    usr = User_info.query.filter_by(email='admin@ds.iitm.ac.in').first()
    if usr:
        usr.role = 0
        db.session.commit()
        print(" Role updated to 0 for admin@ds.iitm.ac.in")
    else:
        print(" User not found for role update")

from backend.controllers import *

print("my_ticketshow_App has started...")

# Run the app
if __name__ == "__main__":
    application.run()