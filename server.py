"""Server for classified messages app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """View homepage to login and show all classifieds."""
    classifieds = crud.get_classifieds()
    print(session)
    return render_template('homepage.html', classifieds=classifieds)

@app.route("/classified/<int:id>")
def show_classified_details(id):
    """View details for a specific classified."""
    classified = crud.get_classified_by_id(id)
    return render_template('classified_details.html', classified=classified)

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
    return redirect("/users/sign_up")

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
    """View details for a specific classified."""
    db_user = crud.get_user_by_id(id)
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
