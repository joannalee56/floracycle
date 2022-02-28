# Floracycle

Floracycle is a web-based marketplace for sharing, recycling, buying and selling floral and gardening services and goods. Floracycle was created to connect local and urban farmers with one another to source materials, share skills and resources, all the while reducing waste.

![Floracycle overview](/static/images/Floracycle1.gif)


## Contents
* [Features](#features)
* [Tech Stack](#tech)
* [Installation](#installation)
* [Demo Link](#demo)
* [Developer Info](#developer)


## <a name="features"></a>Features

- View, post, edit, manage, delete classifieds for plant and floral matter

- Tagging classifieds

- Custom built-in messaging platform

- Upload images

- Search and filter classifieds by distance and location, category tags, min/max price, cost type (for sale/trade/free)


## <a name="tech"></a>Tech Stack

Floracycle employs a combination of technologies to work properly:

- Backend: Python, Flask, SQLAlchemy, PostgreSQL 
- Frontend: Javascript, HTML/CSS, Twitter Bootstrap, jQuery, AJAX
- APIs: Google Maps API, Cloudinary API
- Libraries: pgeocode, Faker


## <a name="installation"></a>Installation

Floracycle requires Python, Flask-SQLAlchemy, psycopg2-binary, and PostgreSQL to run.


To start your installation, clone the floracycle repo:
```sh
$ git clone https://github.com/joannalee56/floracycle.git
```


Create a virtual environment, activate it, and install the packages required for the app from requirements.txt:
```sh
$ virtualenv env
$ source env/bin/activate
(env) $ pip3 install -r requirements.txt
```


Create a PostgreSQL database:
```sh
(env) $ createdb floracycle
```


Seed the database:
```sh
(env) $ python3 seed_database.py
```


Create a <kbd>secrets.sh</kbd> file in the app's directory and add your API keys as such:
```sh
export GOOGLE_MAPS_KEY="YOUR_KEY_HERE"
export CLOUDINARY_KEY="YOUR_KEY_HERE"
export CLOUDINARY_SECRET="YOUR_KEY_HERE"
```


To verify that it worked, you can use echo to print the value of the API keys to the terminal:
```sh
$ echo $GOOGLE_MAPS_KEY
```


After installing the dependencies, run the server:
```sh
(env) $ python3 server.py
```


Navigate to http://localhost:5000 in your browser and start exploring the app.




## <a name="demo"></a>Demo Link

- [Youtube](https://youtu.be/LvU7Bgee-mU)
<!-- - [AWS](http://35.88.128.246/) -->

## <a name="developer"></a>Developer Info

Floracycle was created with love by Joanna Lee. Joanna is a software engineer in the Bay Area, and you can find her on [LinkedIn](https://www.linkedin.com/in/joanna-e-lee/).


