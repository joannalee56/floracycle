"""CRUD operations."""

from model import db, User, Classified, Message, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def update_user(db_user):
    """Edit and update user profile."""

    db.session.add(db_user)
    db.session.commit()

    return db_user


def create_classified(user_id, post_title, description, cost, cost_type, postal_code, post_image=None):
    """Create and return a new classified."""

    classified = Classified(user_id=user_id, post_title=post_title, description=description, cost=cost, cost_type=cost_type, postal_code=postal_code, post_image=post_image)
    ""
    db.session.add(classified)
    db.session.commit()

    return classified


def get_classifieds():
    return Classified.query.all()

def get_classified_by_id(id):
    return Classified.query.filter(Classified.classified_id == id).one()
    # return Classified.query.get(1)

def get_classified_by_keyword(word):
    # input validation
    return Classified.query.filter( (Classified.post_title.like(f"%{word}%")) | (Classified.description.like(f"%{word}%")) ).order_by('post_time').all()

def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.filter(User.user_id == id).one()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_password(email):
    user = get_user_by_email(email)
    return user.password

def create_message(message):
    """Create and return a new classified."""
    message = Message(message=message)

    db.session.add(message)
    db.session.commit()

    return message



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
