"""Server for classifieds app."""

from curses import keyname
from distutils.log import debug
from sqlite3 import dbapi2
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from itsdangerous import json

from model import Classified, connect_to_db
import crud

from jinja2 import StrictUndefined

import os
import cloudinary.uploader
import requests


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

MAPS_API_KEY = os.environ['GOOGLE_MAPS_KEY']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "floracycle"

socketIo = SocketIO(app)


@app.route("/")
def show_homepage():
    """View homepage to login and show all classifieds."""

    search = request.args.get("search")
    if search is None: 
        search = ""
    session["search"] = search
    if search: 
        classifieds = crud.get_classified_by_keyword(search)
    else:
        classifieds = crud.get_classifieds()

    return render_template('homepage.html', classifieds=classifieds, search=search, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/search/category")
def filter_classifieds():
    """Show all classifieds with filtered categories."""
    # Search keyword in title, description, and category tag
    search = session["search"]
    classifieds = crud.get_classified_by_keyword(search)
    print()
    print("*************")
    print(f"search ={search}")
    print()

    search_to_return = []
    # Search filter by tag
    filtered_tags = []
    tagged_classifieds = []
    if request.args.getlist("tag_id"):
        lst_of_tag_ids = request.args.getlist("tag_id")
        for id in lst_of_tag_ids:
            tag_classifieds = crud.get_classified_by_tag(id)
            tagged_classifieds += tag_classifieds
        for tagged in tagged_classifieds:
            if(tagged in classifieds):
                filtered_tags.append(tagged)
    else:
        filtered_tags = classifieds
    filtered_tags = set(filtered_tags)

    # Search filter by cost type
    if request.args.get("cost-type"):
        cost_type = request.args.get("cost-type")
        filtered_cost_type = set(crud.get_classified_by_cost_type(cost_type))
    else:
        filtered_cost_type = set(classifieds)

    # Search filter by min and max price
    if request.args.get("price-min"):
        price_min = int(request.args.get("price-min"))
    else:
        price_min = 0
    if request.args.get("price-max"):
        price_max = int(request.args.get("price-max"))
    else:
        price_max = 1000000

    filtered_cost = set(crud.get_classified_by_cost(price_min, price_max))

    # Search filter by haversine miles from zipcode 
    filtered_miles = []
    if request.args.get("miles"):
        input_miles = int(request.args.get("miles"))
    else:
        input_miles = 100000000000000

    if request.args.get("zip"):
        input_zip = int(request.args.get("zip"))
        for classified in classifieds:
            haversine_miles = crud.get_distance_in_miles(input_zip, classified.postal_code)
            if (input_miles >= haversine_miles):
                filtered_miles.append(classified)
    else:
        filtered_miles = classifieds

    search_to_return = list(filtered_cost_type & filtered_tags & filtered_cost & set(classifieds) & set(filtered_miles))

    return render_template('filtered.html', classifieds=search_to_return)


@app.route("/search/")
def show_final_search():
    """View search after filters."""

    search = request.args.get("search")
    if search is None: 
        search = ""
    session["search"] = search
    if search: 
        classifieds = crud.get_classified_by_keyword(search)
    else:
        classifieds = crud.get_classifieds()
    
    return render_template('homepage.html', classifieds=classifieds, search=search, MAPS_API_KEY=MAPS_API_KEY)


@app.route("/classified/<int:classified_id>")
def show_classified_details(classified_id):
    """View details for a specific classified."""
    classified = crud.get_classified_by_id(classified_id)
    
    classified_gregorian_date = crud.get_classified_gregorian_date(classified_id)
    user_gregorian_date = crud.get_user_gregorian_date(classified.user)

    return render_template('classified_details.html', classified=classified, classified_gregorian_date=classified_gregorian_date, user_gregorian_date=user_gregorian_date, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/classified/new")
def show_new_classified():
    """Show form to post new classified."""
    return render_template("new_classified.html")

@app.route("/classified/new/post", methods=['POST'])
def post_new_classified():
    """Post new classified data."""

    user_id = session["user_id"]
    post_title = (request.form.get("post_title")).lower()
    tag_ids = request.form.getlist("tag")
    description = request.form.get("description")
    cost = request.form.get("cost")
    if cost == "":
        cost = 0
    cost_type = request.form.get("cost_type")
    if request.form.get("postal_code") == "":
        postal_code = 0
    else: 
        postal_code = int(request.form.get("postal_code"))
    post_image = request.files["post_image"]

    # Sprint 2: user input validation
    # WTForms (since spaces instead of None), check if input is none and other test cases
    if post_title == None:
        flash ("Title of classified required. Please enter information of the floral matter you are posting.")
        return redirect('/classified/new/post')
    elif postal_code == None:
        flash ("Location of classified required. Please enter where this is located.")
        return redirect('/classified/new/post')
    elif post_image:
        result = cloudinary.uploader.upload(post_image,
                                            api_key = CLOUDINARY_KEY,
                                            api_secret = CLOUDINARY_SECRET,
                                            cloud_name = CLOUD_NAME)
        img_url = result['secure_url']
        classified = crud.create_classified(user_id=user_id, post_title=post_title, description=description, 
                                            cost=cost, cost_type=cost_type, postal_code=postal_code, tag_ids=tag_ids, post_image=img_url)
    else:
        classified = crud.create_classified(user_id=user_id, post_title=post_title, description=description, 
                                            cost=cost, cost_type=cost_type, postal_code=postal_code, tag_ids=tag_ids)
    
    return redirect(f"/classified/{classified.classified_id}")

@app.route("/login")
def show_login():
    """Show login form."""

    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_user():
    """Log in user."""
    input_email = request.form.get("email")
    input_password = request.form.get("password")
    db_user = crud.get_user_by_email(input_email)

    classified_list = []

    classified_set = set()
    for message in db_user.messages_sender:
        classified_set.add(message.classified)
    for message in db_user.messages_recipient:
        classified_set.add(message.classified)

    for classified in classified_set:
        classified_list.append(classified.to_dict())

    if db_user is None:
        flash ("There is no such user. Please enter a valid email.")
        return redirect('/login')

    if input_password != db_user.password:
        flash("Wrong password. Please try again.")
        return redirect("/login")
    else:
        session["user_id"] = db_user.user_id
        # flash(f"Logged in as {db_user.email}")

        return render_template('user_profile.html', db_user=db_user, classified_list=classified_list)

@app.route("/users/sign_up")
def show_signup():
    """Show signup form."""
    return render_template("signup.html")

@app.route("/users/sign_up", methods=['POST'])
def register_user():
    """Create new user."""
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    if crud.get_user_by_email(email):
        flash("This email already exists. Please login or try a new email.")
    else:
        crud.create_user(fname, lname, email, password)
        flash("Account created successfully. Please log in.")
    return redirect('/login')

@app.route("/users/password/new")
def show_forgotpassword():
    """Show forgot password form."""
    return render_template("forgot_password.html")

@app.route("/users/password/new", methods=['POST'])
def send_password():
    """If password exists in system, send forgotten password."""

    input_email = request.form.get("email")
    db_user = crud.get_user_by_email(input_email)

    if db_user is None:
        flash ("Email not found. Please create an account.")
        return redirect('/login')
    else:
        sent_pw_message = (f"Post sent to {db_user.email}.")
        return render_template("sent_password.html", db_user=db_user, sent_pw_message=sent_pw_message)

#find library for sending emails for forgotten passwords

@app.route("/users")
def show_users():
    """View all users."""
    users = crud.get_users()
    return render_template('all_users.html', users=users)

@app.route("/user/<int:user_id>")
def show_user_profile(user_id):
    """View details for a user's profile."""
    db_user = crud.get_user_by_id(user_id)

    classified_list = []

    classified_set = set()
    for message in db_user.messages_sender:
        classified_set.add(message.classified)
    for message in db_user.messages_recipient:
        classified_set.add(message.classified)

    for classified in classified_set:
        classified_list.append(classified.to_dict())
    
    return render_template('user_profile.html', db_user=db_user, classified_list=classified_list)


@app.route("/user/<int:user_id>/messages/yourlistings/classified<int:classified_id>/sender<int:sender_id>")
def show_messages_your_listings(user_id, classified_id, sender_id):
    """Show messages of your listings."""
    user_id = session["user_id"]
    db_user = crud.get_user_by_id(user_id)

    print("*************")
    print("*************")
    print("db_user.messages_recipient")
    print(db_user.messages_recipient)

    classified = crud.get_classified_by_id(classified_id)
    classified_id = classified.classified_id

    for message in db_user.messages_recipient:
        sender = message.sender
        message_time = message.message_time

    print("*************")
    print("*************")
    print("sender")
    print(sender)

    # sender_id = classified.messages[0].sender_id

    # classified_list = []
    # Get all messages of classified from sender and recipient
    # Convert to set
    # classified_set = set()
    # for message in db_user.messages_recipient:
    #     classified_set.add(message.classified)
    
    # classified_dictionary = {}
    # date key
    # value dict: message, sender, id/name
    # Add set to list of dictionary
    # for classified in classified_set:
    #     classified_list.append(classified.to_dict())
    


    # Get list of Sender names from classified's messages
    # classified_list_from_set = list(classified_set)
    # sender_name = []
    # for classified in classified_list_from_set:
    #     get messages by classified id and 
    #         sender_name.append(message.sender.fname)

    
    classified_gregorian_date = crud.get_classified_gregorian_date(classified_id)


    your_listing_messages = crud.get_messages_by_classified_id(classified_id, sender_id, recipient_id=user_id) 
    print("*************")
    print("your_listing_messages")
    print(your_listing_messages)


    return render_template('messages_your_listings.html', db_user=db_user, sender=sender, classified=classified, classified_gregorian_date=classified_gregorian_date, your_listing_messages=your_listing_messages, message_time = message_time)

@app.route('/user/<int:user_id>/messages/yourlistings/classified<int:classified_id>/sender<int:sender_id>/send', methods=["POST"])
def send_message_from_your_listings(user_id, classified_id, sender_id):
    """Send messages from Your Inquiries to the backend."""
    message = request.json.get("message")
    print("*************")
    print("message")
    print(message)
    classified = crud.get_classified_by_id(classified_id)
    
    user_id = session["user_id"]
    sender_id = classified.messages[0].sender_id
    print("*************")
    print("sender_id")
    print(sender_id)

    db_user = crud.get_user_by_id(user_id)
    db_user_dict = {"image": db_user.image, "fname": db_user.fname }
    message_object = crud.create_message(user_id, sender_id, classified_id, message)

    message_time = message_object.message_time.strftime("%-m/%-d/%Y %I:%M %p")

    return jsonify({ 'message': message, 'message_time': message_time, 'db_user': db_user_dict })

@app.route("/user/<int:user_id>/messages/yourinquiries/classified<int:classified_id>/sender<int:sender_id>")
def show_messages_your_inquiries(user_id, classified_id, sender_id):
    """Show messages of your inquiries."""
    user_id = session["user_id"]
    db_user = crud.get_user_by_id(user_id)

    print("*************")
    print("user_id")
    print(user_id)

    print("*************")
    print("db_user.messages_sender")
    print(db_user.messages_sender)

    for message in db_user.messages_sender:
        print("*************")
        print("message.recipient_id")
        print(message.recipient_id)
        inq_recipient = message.recipient
        inq_recipient_id = message.recipient_id
        message_time = message.message_time

    classified = crud.get_classified_by_id(classified_id)
    classified_id = classified.classified_id

    classified_gregorian_date = crud.get_classified_gregorian_date(classified_id)


    # inq_recipient = crud.get_user_by_id(inq_recipient_id)
    your_inquiries_messages = crud.get_messages_by_classified_id(classified_id, sender_id=user_id, recipient_id=inq_recipient_id)

    print("*************")
    print("your_inquiries_messages")
    print(your_inquiries_messages)

    return render_template('messages_your_inquiries.html', db_user=db_user, inq_recipient_id=inq_recipient_id, classified=classified, classified_gregorian_date=classified_gregorian_date, your_inquiries_messages=your_inquiries_messages, inq_recipient=inq_recipient, message_time=message_time, MAPS_API_KEY=MAPS_API_KEY)


@app.route('/user/<int:user_id>/messages/yourinquiries/classified<int:classified_id>/sender<int:sender_id>/send', methods=["POST"])
def send_message_from_your_inquiries(user_id, classified_id, sender_id):
    """Send messages from Your Inquiries to the backend."""
    message = request.json.get("message")
    print("*************")
    print("message")
    print(message)
    classified = crud.get_classified_by_id(classified_id)
    
    user_id = session["user_id"]
    sender_id = classified.user.user_id
    print("*************")
    print("sender_id")
    print(sender_id)

    db_user = crud.get_user_by_id(sender_id)
    db_user_dict = {"image": db_user.image, "fname": db_user.fname }
    message_object = crud.create_message(user_id, sender_id, classified_id, message)

    message_time = message_object.message_time.strftime("%-m/%-d/%Y %I:%M %p")

    return jsonify({ 'message': message, 'message_time': message_time, 'db_user': db_user_dict })


@app.route("/user/<int:user_id>/edit")
def edit_user_profile(user_id):
    """Show form to edit user profile."""
    db_user = crud.get_user_by_id(user_id)
    return render_template("edit_user_profile.html", db_user=db_user)


@app.route("/user/<int:user_id>/edit/post", methods=["POST"])
def post_user_profile_changes(user_id):
    """Edit and save details of a user's profile page and return to profile page with saved data."""
    db_user = crud.get_user_by_id(user_id)
    print("db_user***************************")
    print(db_user)

    db_user.fname = request.form.get("fname")
    db_user.lname = request.form.get("lname")
    db_user.address1 = request.form.get("address1")
    db_user.address2 = request.form.get("address2")
    db_user.city = request.form.get("city")
    db_user.state = request.form.get("state")

    if request.form.get("zip"):
        db_user.zip = request.form.get("zip")
    else: 
        db_user.zip = 0
    db_user.phone = request.form.get("phone")
    db_user.about_me = request.form.get("about_me")
    db_user.web = request.form.get("web")
    db_user.ig = request.form.get("ig")
    db_user.fb = request.form.get("fb")
    image = request.files["image"]

    if image:
        result = cloudinary.uploader.upload(image,
                                            api_key = CLOUDINARY_KEY,
                                            api_secret = CLOUDINARY_SECRET,
                                            cloud_name = CLOUD_NAME)
        db_user.image = result['secure_url']
        crud.update_user(db_user) 
    else:
        crud.update_user(db_user)
    
    return redirect(f"/user/{db_user.user_id}")

@app.route("/classified/<int:classified_id>/published/edit")
def show_published_classified_edit_form(classified_id):
    """Show in user settings: form to edit already published classified."""
    classified = crud.get_classified_by_id(classified_id)

    classified_gregorian_date = crud.get_classified_gregorian_date(classified_id)
    user_gregorian_date = crud.get_user_gregorian_date(classified.user)

    tag_list = []
    for tag in classified.tags:
        tag_list.append(tag.tag_label)

    return render_template('edit_published_classified.html', classified=classified, classified_gregorian_date=classified_gregorian_date, user_gregorian_date=user_gregorian_date, tag_list=tag_list, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/classified/<int:classified_id>/published/edit/post", methods=["POST"])
def publish_new_classified_changes(classified_id):
    """Edit and save a published classified. Return to classifieds page with saved data."""
    classified = crud.get_classified_by_id(classified_id)

    classified.post_title = request.form.get("post_title")
    tag_ids = request.form.getlist("tag")

    classified.tag_list = []
    for tag_id in tag_ids:
        classified.tag_list.append(crud.get_tag(tag_id))
    classified.tags = classified.tag_list

    classified.description = request.form.get("description")
    classified.cost = request.form.get("cost")
    classified.cost_type = request.form.get("cost_type")
    classified.postal_code = request.form.get("postal_code")
    classified.location = crud.get_city_state(classified.postal_code)
    classified_image = request.files["post_image"]

    if classified_image:
        result = cloudinary.uploader.upload(classified_image,
                                            api_key = CLOUDINARY_KEY,
                                            api_secret = CLOUDINARY_SECRET,
                                            cloud_name = CLOUD_NAME)
        classified.post_image = result['secure_url']

    crud.update_classified(classified)
    return redirect(f"/classified/{classified.classified_id}")



@app.route("/classified/<int:classified_id>/published/delete")
def delete_published_classified(classified_id):
    """In user settings: delete already published classified. If classified exists, delete it."""
    user_id = session["user_id"]
    classified = crud.get_classified_by_id(classified_id)
    print("*********")
    print(classified)
    if classified: 
        crud.delete_classified(classified)
        print("*********")
        print(classified)
    return redirect(f"/user/{user_id}")


@app.route("/logout")
def logout():
    """Logout."""
    session.pop("user_id")

    # flash(f"Logged out.")
    return redirect('/')

@app.route("/classified/<int:classified_id>/message")
def show_message_form(classified_id):
    """Show form to send message to florist about classified."""
    sender_id = session["user_id"]
    db_user = crud.get_user_by_id(sender_id)

    classified = crud.get_classified_by_id(classified_id)
    recipient_id = classified.user.user_id
    classified_gregorian_date = crud.get_classified_gregorian_date(classified_id)
    user_gregorian_date = crud.get_user_gregorian_date(classified.user)

    messages = crud.get_messages_by_classified_id(classified_id, sender_id, recipient_id)

    return render_template('messages_from_classifieds.html', db_user=db_user, classified=classified, classified_gregorian_date=classified_gregorian_date, user_gregorian_date=user_gregorian_date, messages=messages, MAPS_API_KEY=MAPS_API_KEY)

@app.route('/classified/<int:classified_id>/send/message', methods=["POST"])
def send_message_from_classifieds(classified_id):
    """Send message to the backend."""
    message = request.json.get("message")
    print("*************")
    print("message")
    print(message)
    classified = crud.get_classified_by_id(classified_id)
    sender_id = session["user_id"]
    recipient_id = classified.user.user_id
    print("*************")
    print("sender_id")
    print(sender_id)

    db_user = crud.get_user_by_id(sender_id)
    db_user_dict = {"image": db_user.image, "fname": db_user.fname }
    message_object = crud.create_message(sender_id, recipient_id, classified_id, message)
    message_time = message_object.message_time.strftime("%-m/%-d/%Y %-I:%M %p")
    print("*************")
    print("message_time")
    print(message_time)

    return jsonify({ 'message': message, 'message_time': message_time, 'db_user': db_user_dict })
    # return redirect(f'/classified/{classified.classified_id}/message')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

