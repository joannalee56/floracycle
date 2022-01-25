"""CRUD operations."""

from model import db, User, Classified, Message, Tag, Classified_Tag, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)
    
    db.session.add(user)
    db.session.commit()

    return user

def create_user_from_seed(fname, lname, email, password, address1, address2, city, state, zip, phone, about_me, image):
    """Update user."""

    user = User(fname=fname, lname=lname, email=email, password=password, address1=address1, address2=address2, city=city, state=state, zip=zip, phone=phone, about_me=about_me, image=image)
    
    db.session.add(user)
    db.session.commit()

    return user

def update_user(db_user):
    """Edit and update user profile."""

    db.session.add(db_user)
    db.session.commit()

    return db_user


def create_classified(user_id, post_title, description, cost, cost_type, postal_code, tag_ids, post_image=None):
    """Create and return a new classified."""
    
    tag_list = []
    for tag_id in tag_ids:
        tag_list.append(Tag.query.get(int(tag_id)))

    classified = Classified(user_id=user_id, post_title=post_title, description=description, cost=cost, cost_type=cost_type, postal_code=postal_code, post_image=post_image)
    classified.tags.extend(tag_list)

    db.session.add(classified)
    db.session.commit()

    return classified

def create_tag(tag_label):
    """Create and return a new tag."""

    tag = Tag(tag_label=tag_label)
    
    db.session.add(tag)
    db.session.commit()

    return tag

def create_message(message):
    """Create and return a new classified."""
    message = Message(message=message)

    db.session.add(message)
    db.session.commit()

    return message
    
def get_classifieds():
    return Classified.query.all()

def get_classified_by_id(id):
    return Classified.query.filter(Classified.classified_id == id).one()
    # return Classified.query.get(1)

def get_classified_by_keyword(word):
    # input validation
    return db.session.query(Classified).filter(Classified.post_title.like(f"%{word}%") | Classified.description.like(f"%{word}%")).order_by('post_time').all()
    # Classified.query.filter( (Classified.post_title.like(f"%{word}%")) | (Classified.description.like(f"%{word}%")) ).order_by('post_time').all()

def get_classified_by_tag(tag_id):
    results = Tag.query.get(tag_id).classifieds
    return results
    # return db.session.query(Classified).filter(Tag.tag_label.like(f"%{word}%")).all()
    # c = db.session.query(Classified).filter(Tag.tag_label.like("indoor")).all()

def get_classified_by_cost_type(cost_type):
    return Classified.query.filter(Classified.cost_type == cost_type).all()

def get_classified_by_price_min(price_min):
    return Classified.query.filter(Classified.cost > price_min).all()

def get_classified_by_price_max(price_max):
    return Classified.query.filter(Classified.cost < price_max).all()



def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.filter(User.user_id == id).one()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_password(email):
    user = get_user_by_email(email)
    return user.password



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
