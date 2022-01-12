"""Seed the database."""

import os 
import json
from random import choice, randint
from datetime import datetime
import server, model, crud
from faker import Faker
from faker.providers import internet


os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load classifieds data from JSON file
with open('data/classifieds.json') as f:
    classifieds_data = json.loads(f.read())

fake = Faker()
fake.add_provider(internet)
# Create sample classifieds, store them in list that we can add to later
# and create a search function for.

classifieds_in_db = []
for classified in classifieds_data:
    # Get the title, overview, and image_path from the classified
    # dictionary. Then, get the post_time and convert it to a
    # datetime object with datetime.strptime
    
    description = classified["description"]
    post_image = classified["post_image"]
    post_time = datetime.strptime(classified["post_time"], "%Y-%m-%d")
    post_title = classified["post_title"]

    new_classified = crud.create_classified(post_title, description, post_time, post_image)
    classifieds_in_db.append(new_classified)


# Create fake emails and passwords
fake_email = []
fake_password = []
for n in range(10):
    email = fake.free_email()
    password = fake.password()
    user = crud.create_user(email, password)

    # Create 10 ratings for the user
    all_classifieds = model.Classified.query.all()
    # all_classifieds = classifieds_in_db
    for m in range(10):
        random_classified = choice(all_classifieds)
        random_rating = randint(1,5)
        rating = crud.create_rating(user,random_classified, random_rating)