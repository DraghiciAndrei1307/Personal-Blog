# Personal-Blog

## Description

This is my personal blog web application solution. If you want to check it you can either clone this repo (please 
follow the steps described in the `Hot to use` section) and try it yourself, or you can check the deployed version on: 
https://andrei-draghici-personal-website.onrender.com/  

## How to use

There are 2 ways of using this web application app: 
    
    - host is on a private VM on your local network
    - use a dedicated VPS and deploy this application on the Internet (this is the option I currently use)


### Host on a private VM on your local home network

### Host on a dedicated VPS

## Development steps

1) Create the Flask application and integrate the CKEditor and Bootstrap within the Flask application

```python
app = Flask(__name__) # create the Flask application for the __name__ file 
                      # which is the current file if we directly run this file
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY') # the secret key is needed for CSRF protection; this is useful 
                                                       # for WTForms
# We integrate the CKEditor and Bootstrap into our Flask app
ckeditor = CKEditor(app) 
Bootstrap(app)
```

2) Configure Flask-Login

```python
# Configure Flask-Login

login_manager = LoginManager()
login_manager.init_app(app)
```

We use the flask_login package to import the LoginManager() class. This login manager helps us to secure routes and 
load different users by ID.

3) Create Database

```python
# CREATE DATABASE
class Base(DeclarativeBase): # base model class we will use for our models
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db") # connection string for 
                                                                                       # the database 
db = SQLAlchemy(model_class=Base) # create a d
db.init_app(app)
```

We use the SQLAlchemy ORM (Object-relational mapping) to configure the database for our Flask application.

First, we create the Base class which will be used as a base for our future models (Python classes that inherit the 
Base class) which we will use to create tables in our database. 

After, we configure the database URI to connect to our database. We get the URI value from the DB_URI env variable. If 
this env variable does not exist, we use the `sqlite:///posts.db`. 

The DB_URI should contain something like this: `postgresql://user:password@localhost/dbname` if we are talking of 
production databases like PostgreSQL. 

In our case, if we do not have a production database, a file named posts.db will be created locally. This thing is 
great for test purposes. 

In the end, we are creating an object named `db`, which is an instance of the SQLAlchemy class. We also integrate this 
object with our Flask Application.  

4) Create your models and create your database tables

```python
# CONFIGURE TABLES

# User model to create a table for all registered users.

class User(UserMixin, db.Model): # UserMixin contains some special attributes and methods required for the log in

    ...

# BlogPost model to create a table for all blog posts created by the admin users

class BlogPost(db.Model):

    ...

# Comment model to create a table for all comments created by registered users

class Comment(db.Model):

    ...

with app.app_context():
    db.create_all()
```

In the code snippet above we create 3 models: User, BlogPost and Comment. The relations between them can be viewed in 
the `docs > schema.png` image. 

5) Create user_loader callback

```python
# Create user_loader callback

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()
```

This callback is used to reload the user object from the user ID stored in the session. 


6) Configure the routes 

We have the following routes configured:

    - '/' # GET
    - '/register' # GET & POST
    - '/login' # GET & POST
    - '/logout' # GET
    - '/post/<int:post_id>' # GET & POST
    - '/new-post' # GET & POST
    - '/edit-post/<int:post_id>' # GET & POST
    - '/delete/<int:post_id>' # GET & POST
    - '/about' # GET
    - '/contact' # GET

Because it will take a really long time and will be redundant to discuss all the routes above, we will have a look over 
just `one` route, namely the `/register` route.


```python
# Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

        # check if the email exists inside the database User table

        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()

        if user:
            flash('This email address is already registered', 'danger')
            return redirect(url_for('login'))

        # if the email address is new, we simply add the new user

        new_user = User(email = form.email.data, password = salted_password, name = form.name.data)

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html", form=form)
```

To define this route, we used the `app.route` decorator, a function that we used to decorate the `register` function. 
The `app.route` decorator has the following parameters: a string that sets the route and a list of the requests types 
(`GET` and `POST`) accepted by this route. 

The register function has 2 main functionalities, depending on the request received:
    
- render the `register.html` file when a GET request is detected
    
- if the form (presented in the code snippet below) is submitted, we salt and hash (using the 
`generate_password_hash` function from the `werkzeug.security` package) the password and then we save it inside 
the User table inside our database alongside the other data provided by the user. In the end, we redirect to the 
'/login' route so that the new user can log in.  

```html
 <form action = "{{ url_for('register') }}" method="POST" novalidate>
     {{ form.hidden_tag() }}
     {{ form.email.label }} <br> {{ form.email(type="email", class="form-control", style="width: 100%;", maxlength=200) }} <br>
     {{ form.password.label }} <br> {{ form.password(type="password", class="form-control", style="width: 100%;", maxlength=200) }} <br>
     {{ form.name.label }} <br> {{ form.name(type="name", class="form-control", style="width: 100%;", maxlength=200) }} <br>
     {{ form.submit }}
 </form>
```
