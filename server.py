"""Server for classified ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



# Replace this with routes and view functions!
@app.route('/')
def show_homepage():
    """View homepage to login and show all classifieds."""
    classifieds = crud.get_classifieds()
    return render_template('homepage.html', classifieds=classifieds)

@app.route('/classified/<int:id>')
def show_classified_details(id):
    """View details for a specific classified."""
    classified = crud.get_classified_by_id(id)
    return render_template('classified_details.html', classified=classified)

@app.route('/users')
def show_users():
    """View all users."""
    users = crud.get_users()
    return render_template('all_users.html', users=users)

@app.route('/users', methods=['POST'])
def register_user():
    """Create new user."""
    email = request.form.get("email")
    password = request.form.get("password")
    if crud.get_user_by_email(email):
        flash("This email already exists. Please try again.")
    else:
        crud.create_user(email, password)
        flash("Account created successfully. Please log in.")
    return redirect("/")

@app.route('/login', methods=['POST'])
def login_user():
    """Handle the submission and log in user."""
    email = request.form.get("email")
    input_password = request.form.get("password")
    db_password = crud.get_user_by_password(email)
    
    # if user.password != password:
    if input_password != db_password:
        flash("Please try again.")
    else:
        flash("Logged in!")
    return redirect("/")

@app.route('/user/<int:id>')
def show_user_profile(id):
    """View details for a specific classified."""
    user = crud.get_user_by_id(id)
    return render_template('userprofile.html', user=user)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
