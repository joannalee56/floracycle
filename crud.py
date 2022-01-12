"""CRUD operations."""

from model import db, User, Classified, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_classified(post_title, description, post_time, post_image):
    """Create and return a new classified."""

    classified = Classified(post_title=post_title, description=description, post_time=post_time, post_image=post_image)
    ""
    db.session.add(classified)
    db.session.commit()

    return classified

def get_classifieds():
    return Classified.query.all()

def get_classified_by_id(id):
    return Classified.query.filter(Classified.classified_id == id).one()
    # return Classified.query.get(1)

def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.filter(User.user_id == id).one()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_password(email):
    user = get_user_by_email(email)
    return user.password

def create_rating(user, classified, rating):
    """Create and return a new classified."""
    rating = Rating(user=user, classified=classified, score=rating)

    db.session.add(rating)
    db.session.commit()

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
