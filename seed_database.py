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

    new_classified = crud.create_classified(user_id=user_id, post_title=post_title, description=description, cost=cost, cost_type=cost_type, postal_code=postal_code, post_image=post_image)
    classifieds_in_db.append(new_classified)


# Create fake emails and passwords
for n in range(10):
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.free_email()
    password = fake.password()
    about_me = fake.paragraph(nb_sentences=5)
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, about_me=about_me, image='/static/images/floracycle_profile1.jpg')

    # Create 10 messages for the user
    all_classifieds = model.Classified.query.all()
    
    message = fake.paragraph(nb_sentences=5)
    crud.create_message(message)