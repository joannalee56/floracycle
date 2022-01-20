"""Server for classified messages app."""

from email import message
from re import L
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

from model import Classified, connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """View homepage to login and show all classifieds."""

    search = request.args.get("search")

    if search: 
        classifieds = crud.get_classified_by_keyword(search)
    else:
        classifieds = crud.get_classifieds()
    return render_template('homepage.html', classifieds=classifieds, search=search)

@app.route("/classified/<int:id>")
def show_classified_details(id):
    """View details for a specific classified."""
    classified = crud.get_classified_by_id(id)
    return render_template('classified_details.html', classified=classified)

@app.route("/classified/new")
def create_new_classified():
    """Show form to post new classified."""
    return render_template("new_classified.html")

@app.route("/classified/new/post")
def post_new_classified():
    """Post new classified data."""

    user_id = session["user_id"]
    post_title = request.args.get("post_title")
    description = request.args.get("description")
    cost = request.args.get("cost")
    cost_type = request.args.get("cost_type")
    postal_code = request.args.get("postal_code")
    post_image = request.args.get("post_image")

    # Sprint 2: user input validation
    # WTForms (since spaces instead of None), check if input is none and other test cases
    if post_title == None:
        flash ("Title of classified required. Please enter information of the floral matter you are posting.")
        return redirect('/classified/new/post')
    elif postal_code == None:
        flash ("Location of classified required. Please enter where this is located.")
        return redirect('/classified/new/post')
    else:
        classified = crud.create_classified(user_id=user_id, post_title=post_title, description=description, cost=None, cost_type=cost_type, postal_code=None, post_image='/static/images/floracycle_classifieds_default.jpg')
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
        return render_template('userprofile.html', db_user=db_user)

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

@app.route("/user/<int:id>")
def show_user_profile(id):
    """View details for a user's profile."""
    db_user = crud.get_user_by_id(id)
    return render_template('userprofile.html', db_user=db_user)

@app.route("/user/<int:id>/edit", methods=["POST"])
def edit_user_profile(id):
    """Edit and save details of a user's profile page and return saved data."""
    db_user = crud.get_user_by_id(id)
    print("db_user***************************")
    print(db_user)

    db_user.fname = request.json.get("fname")
    db_user.lname = request.json.get("lname")
    db_user.address1 = request.json.get("address1")
    db_user.address2 = request.json.get("address2")
    db_user.city = request.json.get("city")
    db_user.state = request.json.get("state")
    print("***************************")
    print(db_user.state)
    db_user.zip = request.json.get("zip")
    db_user.phone = request.json.get("phone")
    db_user.about_me = request.json.get("about_me")
    db_user.image = request.json.get("image")

    updated_user = crud.update_user(db_user)
    print("***************************")
    print(db_user)
    return render_template('userprofile.html', db_user=db_user)

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
