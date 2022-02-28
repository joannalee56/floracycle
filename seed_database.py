"""Seed the database."""

import os 
import json
from random import choice, randint
from datetime import datetime
import server, model, crud
from faker import Faker
from faker.providers import internet

os.system('dropdb floracycle')
os.system('createdb floracycle')

model.connect_to_db(server.app)
model.db.create_all()

# Load classifieds data from JSON file
with open('data/classifieds.json') as f:
    classifieds_data = json.loads(f.read())

# Initialize Faker generator
fake = Faker()
fake.add_provider(internet)

profile_images = ["/static/images/floracycle_profile1.jpg", "/static/images/floracycle_profile2.jpg", "/static/images/floracycle_profile3.jpg", "/static/images/floracycle_profile4.jpg", "/static/images/floracycle_profile5.jpg", "/static/images/floracycle_profile6.jpg", "/static/images/floracycle_profile7.jpg", "/static/images/floracycle_profile8.jpg", "/static/images/floracycle_profile9.jpg", "/static/images/floracycle_profile10.jpg", "/static/images/floracycle_profile11.jpg", "/static/images/floracycle_profile12.jpg"]
# Create fake users, emails, and passwords
for item in profile_images:
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.free_email()
    password = fake.password()
    address1 = fake.street_address()
    address2 = fake.secondary_address()
    city = fake.city()
    state = fake.state_abbr()
    zip = fake.postcode()
    phone = fake.phone_number()
    about_me = fake.paragraph(nb_sentences=5)
    image = item
    user = crud.create_user_from_seed(fname=fname, lname=lname, email=email, password=password, address1=address1, address2=address2, city=city, state=state, zip=zip, phone=phone, about_me=about_me, image=image, web="", ig="", fb="")

# Create preloaded tags and categories
preloaded_tags = ['wedding', 'succulents', 'outdoor', 'indoor', 'landscaping', 'events']
for tag in preloaded_tags:    
    crud.create_tag(tag)

# Create sample classifieds, store them in list that we can add to later
# and create a search function for.
classifieds_in_db = []
for classified in classifieds_data:
    # Get the title, overview, and image_path from the classified
    # dictionary. Then, get the post_time and convert it to a
    # datetime object with datetime.strptime

    user_id = classified["user_id"]
    post_title = classified["post_title"]
    description = classified["description"]
    cost = classified["cost"]
    cost_type = classified["cost_type"]
    postal_code = classified["postal_code"]
    post_image = classified["post_image"]
    tag_ids = classified["tag_ids"]

    new_classified = crud.create_classified(user_id=user_id, post_title=post_title, description=description, cost=cost, cost_type=cost_type, postal_code=postal_code, tag_ids=tag_ids, post_image=post_image)
    classifieds_in_db.append(new_classified)
