"""Server for classifieds app."""

from sqlite3 import dbapi2
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

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
def filter_classifieds_by_tag():
    """Show all classifieds with chosen tag."""

    search = session["search"]
    classifieds = crud.get_classified_by_keyword(search)
    print("*************")
    print(f"search ={search}")

    #What to do when tag value is None...
    # tag_id = int(request.args.get("tag_id"))
    if request.args.get("tag_id") != None:
        tag_id = int(request.args.get("tag_id"))
        tag_classifieds = set(crud.get_classified_by_tag(tag_id))

    # tag_id_val = request.args.get("tag_id")
    # if tag_id_val:
    #     tag_id = int(tag_id_val)
    #     tag_classifieds = set(crud.get_classified_by_tag(tag_id))

    print("*************")
    print(f"tag_id ={tag_id}")
    print(f"tag_classifieds ={tag_classifieds}")

    cost_type = request.args.get("cost-type")
    cost_classifieds = crud.get_classified_by_cost_type(cost_type)
    print("*************")
    print(f"cost_type ={cost_type}")
    print(f"cost_classifieds ={cost_classifieds}")

    price_min = int(request.args.get("price-min"))
    price_max = int(request.args.get("price-max"))

    input_miles = int(request.args.get("miles"))
    input_zip = int(request.args.get("zip"))

    filtered_tags = []
    # if tag_id:
    #     for classified in classifieds:
    #         if classified in tag_classifieds:
    #             print("************")
    #             print(f"classified.cost_type ={classified.cost_type}")
    #             filtered_tags.append(classified)

    #One or the other works but not both...
    # if there is cost type and tag id chosen
    # if cost_type and tag_id:
    #     for classified in classifieds:
    #         if (classified in tag_classifieds) and (classified.cost_type == cost_type):
    #             print("************")
    #             print(f"classified.cost_type ={classified.cost_type}")
    #             filtered_tags.append(classified)
    
 
    for classified in classifieds:
        haversine_miles = crud.get_distance_in_miles(input_zip, classified.postal_code)
        print("******************")
        print(input_miles)
        print(haversine_miles)
        print(price_min, price_max, classified.cost, classified.cost_type)
        if (classified in tag_classifieds) and (classified.cost_type == cost_type) and (price_min <= classified.cost) and (price_max > classified.cost) and (input_miles >= haversine_miles):
            print("************")
            print(f"classified.cost_type ={classified.cost_type}")
            filtered_tags.append(classified)


    print("*************")
    print(f"filteredtag ={filtered_tags}")
    return render_template('filter_by_tag.html', filtered_tags=filtered_tags)
    # else:
    #     return redirect('/search/category')
    

@app.route("/classified/<int:classified_id>")
def show_classified_details(classified_id):
    """View details for a specific classified."""
    classified = crud.get_classified_by_id(classified_id)
    return render_template('classified_details.html', classified=classified, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/classified/new")
def show_new_classified():
    """Show form to post new classified."""
    return render_template("new_classified.html")

@app.route("/classified/new/post", methods=['POST'])
def post_new_classified():
    """Post new classified data."""

    user_id = session["user_id"]
    post_title = request.form.get("post_title")
    tag_ids = request.form.getlist("tag")
    description = request.form.get("description")
    cost = request.form.get("cost")
    cost_type = request.form.get("cost_type")
    postal_code = request.form.get("postal_code")
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

    if db_user is None:
        flash ("There is no such user. Please enter a valid email.")
        return redirect('/login')

    if input_password != db_user.password:
        flash("Wrong password. Please try again.")
        return redirect("/login")
    else:
        session["user_id"] = db_user.user_id
        flash(f"Logged in as {db_user.email}")
        return render_template('user_profile.html', db_user=db_user)

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
        flash("Account created successfully.")
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
        flash(f"Password sent to {db_user.email}")
        return render_template("sent_password.html", db_user=db_user)

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
    return render_template('user_profile.html', db_user=db_user)

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
    db_user.zip = request.form.get("zip")
    db_user.phone = request.form.get("phone")
    db_user.about_me = request.form.get("about_me")
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
    return render_template('edit_published_classified.html', classified=classified, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/classified/<int:classified_id>/published/edit/post", methods=["POST"])
def publish_new_classified_changes(classified_id):
    """Edit and save a published classified. Return to classifieds page with saved data."""
    classified = crud.get_classified_by_id(classified_id)

    classified.post_title = request.form.get("post_title")
    tag_ids = request.form.getlist("tag")
    classified.tag_list = []
    for tag_id in tag_ids:
        classified.tag_list.append(crud.get_tag(tag_id))
    classified.tags.extend(classified.tag_list)
    
    classified.description = request.form.get("description")
    classified.cost = request.form.get("cost")
    classified.cost_type = request.form.get("cost_type")
    classified.postal_code = request.form.get("postal_code")
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
    flash(f"Logged out.")
    return redirect('/')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
