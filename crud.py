"""CRUD operations."""

from os import stat

from h11 import SEND_RESPONSE
from model import db, User, Classified, Message, Tag, Classified_Tag, connect_to_db
import pgeocode
from datetime import datetime

# Create and update USER profile
def create_user(fname, lname, email, password, address1="", address2="", city="", state="", zip=000000, phone="", about_me="", web="", ig="", fb="", image="/static/images/floracycle_profile_default.jpg"):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, address1=address1, address2=address2, city=city, state=state, zip=zip, phone=phone, about_me=about_me, web=web, ig=ig, fb=fb, image=image)
    
    db.session.add(user)
    db.session.commit()

    return user

def create_user_from_seed(fname, lname, email, password, address1, address2, city, state, zip, phone, about_me, web, ig, fb, image):
    """Create user from seed."""

    user = User(fname=fname, lname=lname, email=email, password=password, address1=address1, address2=address2, city=city, state=state, zip=zip, phone=phone, about_me=about_me, web=web, ig=ig, fb=fb, image=image)
    
    db.session.add(user)
    db.session.commit()

    return user

def update_user(db_user):
    """Edit and update user profile."""

    db.session.add(db_user)
    db.session.commit()

    return db_user

def get_users():
    return User.query.all()

def get_user_by_id(id):
    # return User.query.filter(User.user_id == id).one()
    return User.query.get(id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_password(email):
    user = get_user_by_email(email)
    return user.password



# Create, search, and edit CLASSIFIED
def create_classified(user_id, post_title, description, cost_type, tag_ids, cost=0, postal_code=00000, post_image='/static/images/floracycle_classifieds_default.jpg'):
    """Create and return a new classified."""
    
    tag_list = []
    for tag_id in tag_ids:
        tag_list.append(Tag.query.get(int(tag_id)))
    
    location = get_city_state(postal_code)

    classified = Classified(user_id=user_id, post_title=post_title, description=description, cost=cost, cost_type=cost_type, postal_code=postal_code, location=location, post_image=post_image)
    classified.tags.extend(tag_list)

    db.session.add(classified)
    db.session.commit()

    return classified

def update_classified(classified):
    """Update classified."""

    db.session.add(classified)
    db.session.commit()

    return classified

def get_classifieds():
    return Classified.query.all()

def get_classified_by_id(id):
    # return Classified.query.filter(Classified.classified_id == id).one()
    return Classified.query.get(id)

def get_classified_by_keyword(word):
    # input validation
    combined_title_description_tag = []
    title_and_description = db.session.query(Classified).filter(Classified.post_title.like(f"%{word}%") | Classified.description.like(f"%{word}%")).order_by('post_time').all()
    if word == "wedding":
        tag = get_classified_by_tag(1)
    if word == "succulents":
        tag = get_classified_by_tag(2)
    if word == "outdoor":
        tag = get_classified_by_tag(3)
    if word == "indoor":
        tag = get_classified_by_tag(4)
    if word == "landscaping":
        tag = get_classified_by_tag(5)
    if word == "events":
        tag = get_classified_by_tag(6)
    else: 
        tag = []

    combined_title_description_tag = title_and_description + tag
    return combined_title_description_tag
        
    # Classified.query.filter( (Classified.post_title.like(f"%{word}%")) | (Classified.description.like(f"%{word}%")) ).order_by('post_time').all()

def get_classified_by_tag(tag_id):
    results = Tag.query.get(tag_id).classifieds
    return results
    # return db.session.query(Classified).filter(Tag.tag_label.like(f"%{word}%")).all()
    # c = db.session.query(Classified).filter(Tag.tag_label.like("indoor")).all()

def get_classified_by_cost_type(cost_type):
    return Classified.query.filter(Classified.cost_type == cost_type).all()

def get_classified_by_cost(price_min, price_max):
    return Classified.query.filter(Classified.cost >= price_min, Classified.cost <= price_max).all()

def get_classified_by_miles(input_miles, input_zip):
    return Classified.query.filter(Classified.postal_code ).all()
    input_miles >= haversine_miles

    haversine_miles = get_distance_in_miles(input_zip, filtered.postal_code)

def get_distance_in_miles(zip1, zip2):
    dist = pgeocode.GeoDistance('us')
    miles = dist.query_postal_code(zip1, zip2)
    return miles

def get_classified_gregorian_date(classified_id):
    classified = get_classified_by_id(classified_id)
    gregorian_date = classified.post_time.strftime("%B %-d, %Y")
    return gregorian_date

def get_user_gregorian_date(user):
    gregorian_date = user.created_at.strftime("%B %-d, %Y")
    return gregorian_date

def get_city_state(zip):
    nomi = pgeocode.Nominatim('us').query_postal_code(zip)
    location = str(nomi.place_name) + ", " + str(nomi.state_name) + ", " + str(nomi.postal_code)
    return location

def delete_classified(classified):
    db.session.delete(classified)
    db.session.commit()

# Create TAG
def create_tag(tag_label):
    """Create and return a new tag."""

    tag = Tag(tag_label=tag_label)
    
    db.session.add(tag)
    db.session.commit()

    return tag

def get_tag(tag_id):
    return Tag.query.get(int(tag_id))

# Create MESSAGE
def create_message(sender_id, recipient_id, classified_id, message):
    """Create and return a new classified."""
    message = Message(sender_id=sender_id, recipient_id=recipient_id, classified_id=classified_id, message=message)

    db.session.add(message)
    db.session.commit()

    return message

def get_messages_by_user_id(user_id):
    return Message.query.filter((Message.sender_id == user_id) | (Message.recipient_id == user_id) ).all()

def get_messages_by_classified_id(classified_id, sender_id, recipient_id):
    return Message.query.filter((Message.classified_id == classified_id) & (Message.sender_id == sender_id) & (Message.recipient_id == recipient_id) ).all()

    # Message.query.filter((Message.classified_id == 1) & (Message.sender_id == 11) & (Message.recipient_id == 1) ).all()

def get_messages_by_classified_id_sender_id(classified_id, sender_id):
    return Message.query.filter((Message.classified_id == classified_id) & (Message.sender_id == sender_id)).all()

def get_messages_by_classified_id_recipient_id(classified_id, recipient_id):
    return Message.query.filter((Message.classified_id == classified_id) & (Message.recipient_id == recipient_id)).all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
