from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#  First Entity: User_info
class User_info(db.Model):
    __tablename__ = "user_info"  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, default=1)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)

    #  Foreign key 
    tickets = db.relationship(
        "Ticket",
        cascade="all,delete",
        backref="user_info",
        lazy=True,
        foreign_keys="Ticket.user_id"
    )

#  Second Entity: Theatre
class theatre(db.Model):
    __tablename__ = "theatre" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship("Shows", cascade="all,delete", backref="theatre", lazy=True)

#  Third Entity: Shows
class Shows(db.Model):
    __tablename__ = "shows"  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    ratings = db.Column(db.Integer, default=0)
    ticket_price = db.Column(db.Float, default=0.0)
    date_time = db.Column(db.DateTime, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey("theatre.id"), nullable=False)
    tickets = db.relationship("Ticket", cascade="all,delete", backref="Shows", lazy=True)

#  Fourth Entity: Ticket
class Ticket(db.Model):
    __tablename__ = "ticket"  
    id = db.Column(db.Integer, primary_key=True)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    sl_no = db.Column(db.Integer, default=0)
    ticket_price = db.Column(db.Float, default=0.0)
    date_time = db.Column(db.DateTime, nullable=False)
    user_ratings = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
    Show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), nullable=False)  