"""Models for classified ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#user.ratings
class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50))

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

#movie.ratings
class Classified(db.Model):
    """A classified."""

    __tablename__ = "classifieds"

    classified_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    post_title = db.Column(db.String)
    description = db.Column(db.Text)
    post_time = db.Column(db.DateTime)
    post_image = db.Column(db.String)
    
    def __repr__(self):
        return f'<Classified classified_id={self.classified_id} title={self.post_title} release_date={self.post_time}>'


#rating.movie
#rating.user
class Rating(db.Model):
    """A Rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.Integer)
    classified_id = db.Column(db.Integer, db.ForeignKey('classifieds.classified_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    classified = db.relationship("Classified", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'




def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
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
