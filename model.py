"""Models for classified messages app."""

from email.policy import default
from os import confstr
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(5), nullable=False, default="user")
    created_at = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    phone = db.Column(db.String)
    about_me = db.Column(db.Text)
    image = db.Column(db.Text, default="/static/images/floracycle_profile1.jpg")

    #.classifieds

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>'


class Classified(db.Model):
    """A classified."""

    __tablename__ = "classifieds"

    classified_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))                
    post_title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer)
    cost_type = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    post_time = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    post_image = db.Column(db.String)
    
    user = db.relationship("User", backref="classifieds")

    # get image function

    def __repr__(self):
        return f'<Classified classified_id={self.classified_id} title={self.post_title} cost={self.cost} cost_type={self.cost_type}>'


class Message(db.Model):
    """A message."""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    sender_id = db.Column(db.Integer)
    classified_id = db.Column(db.Integer, db.ForeignKey("classifieds.classified_id"))
    message = db.Column(db.Text)
    message_time = db.Column(db.Date, nullable=False, default=datetime.datetime.now())

    classified = db.relationship("Classified", backref="messages")
    user = db.relationship("User", backref="messages")

    def __repr__(self):
        return f'<Message message_id={self.message_id} message={self.message}>'


class Classified_Tag(db.Model):
    """A classified tag."""

    __tablename__ = "classified_tags"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    classified_id = db.Column(db.Integer, db.ForeignKey("classifieds.classified_id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))
    
    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} tag_label={self.tag_label}>'


class Tag(db.Model):
    """A tag."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    tag_label = db.Column(db.String)

    classifieds = db.relationship("Classified", secondary="classified_tags", backref="tags")
    
    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} tag_label={self.tag_label}>'




def connect_to_db(flask_app, db_uri="postgresql:///floracycle", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
