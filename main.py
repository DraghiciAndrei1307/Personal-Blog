from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
#from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float, Boolean
from functools import wraps

from http import HTTPStatus
#from sqlalchemy.testing.pickleable import User
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, CareerEntryForm, StudiesEntryForm, \
    ProjectsEntryForm, StepForm

from typing import List
from sqlalchemy import ForeignKey

import os

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap(app)

# Configure Flask-Login

login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLES

# User model to create a table for all registered users.

class User(UserMixin, db.Model): # UserMixin contains some special attributes and methods required for the log in
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")

# BlogPost model to create a table for all blog posts created by the admin users

class BlogPost(db.Model):
    __tablename__ = "blog_posts_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("user_table.id"))
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post")

# Comment model to create a table for all comments created by registered users

class Comment(db.Model):

    __tablename__ = "comment_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)

    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts_table.id"))
    post = relationship("BlogPost", back_populates="comments")

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("user_table.id"))
    author = relationship("User", back_populates="comments")


class Career(db.Model):

    __tablename__ = "career_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(250), nullable=False)
    role: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[str] = mapped_column(String(250), nullable=False)
    end_date: Mapped[str] = mapped_column(String(250), nullable=False)
    activity: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Studies(db.Model):

    __tablename__ = "studies_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university: Mapped[str] = mapped_column(String(250), nullable=False)
    faculty: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[str] = mapped_column(String(250), nullable=False)
    end_date: Mapped[str] = mapped_column(String(250), nullable=False)
    grade: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Projects(db.Model):

    __tablename__ = "projects_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    progress_level: Mapped[str] = mapped_column(Float, nullable=False)
    start_date: Mapped[str] = mapped_column(String(250), nullable=False)
    end_date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    steps = relationship("ProjectStep", back_populates="project")

class ProjectStep(db.Model):

    __tablename__ = "project_steps_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    project_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("projects_table.id"))
    project = relationship("Projects", back_populates="steps")

with app.app_context():
    db.create_all()

# Create user_loader callback

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()

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

# Retrieve a user from the database based on their email.
@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        selected_user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()

        if not selected_user:

            flash('Email is incorrect.')

            return redirect(url_for("login"))
        elif not check_password_hash(selected_user.password, form.password.data):
            flash('Invalid password.')
        else:
            login_user(selected_user)
            return redirect(url_for("get_all_posts"))

    return render_template("login.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

#--------------------------------BLOG POSTS----------------------------------------------------------------------------#

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, logged_in = current_user.is_authenticated)

# Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    result = db.session.execute(db.select(Comment))
    comments = result.scalars()

    form = CommentForm()

    if form.validate_on_submit():

        # Add the new entry

        new_comment = Comment(
            text = form.body.data,
            post = requested_post,
            author=current_user,
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("show_post", post_id=post_id, comments=comments, logged_in = current_user.is_authenticated))

    return render_template(
        "post.html",
        post=requested_post,
        logged_in = current_user.is_authenticated,
        form = form,
        comments = comments
    )

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.get_id() != '1':
            abort(HTTPStatus.UNAUTHORIZED)

        return f(*args, **kwargs)

    return decorated_function

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in = current_user.is_authenticated)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template(
        "make-post.html",
        form=edit_form,
        post_id=post_id,
        is_edit=True,
        logged_in = current_user.is_authenticated
    )

@app.route("/delete/post/<int:post_id>")
@admin_only
@login_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

#----------------------------------------------------------------------------------------------------------------------#

#--------------------------------CAREER--------------------------------------------------------------------------------#

@app.route("/career")
def career():
    result = db.session.execute(db.select(Career))
    career_entries = result.scalars().all()
    return render_template(
        "career.html",
        career_entries=career_entries,
        logged_in=current_user.is_authenticated
    )

@app.route("/career/<int:career_entry_id>")
def show_career_entry(career_entry_id):

    selected_career_entry = db.get_or_404(Career, career_entry_id)

    return render_template(
        "career_entry.html",
        career_entry=selected_career_entry,
        logged_in = current_user.is_authenticated)

@app.route("/new-career-entry", methods=["GET", "POST"])
@admin_only
@login_required
def add_new_career_entry():

    form = CareerEntryForm()

    if form.validate_on_submit():

        new_career_entry = Career(
            organization_name=form.organization_name.data,
            role=form.role.data,
            img_url=form.img_url.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            activity=form.activity.data,
        )

        db.session.add(new_career_entry)
        db.session.commit()

        return redirect(url_for("career"))


    return render_template(
        "make-career-entry.html",
        is_edit=False,
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/edit-career-entry/<int:career_entry_id>", methods=["GET", "POST"])
@admin_only
@login_required
def edit_career_entry(career_entry_id):

    selected_career_entry = db.get_or_404(Career, career_entry_id)

    form = CareerEntryForm(
        organization_name=selected_career_entry.organization_name,
        role=selected_career_entry.role,
        img_url=selected_career_entry.img_url,
        start_date=selected_career_entry.start_date,
        end_date=selected_career_entry.end_date,
        activity=selected_career_entry.activity,
    )

    if form.validate_on_submit():
        selected_career_entry.organization_name = form.organization_name.data
        selected_career_entry.role = form.role.data
        selected_career_entry.img_url = form.img_url.data
        selected_career_entry.start_date = form.start_date.data
        selected_career_entry.end_date = form.end_date.data
        selected_career_entry.activity = form.activity.data
        db.session.commit()

        return redirect(url_for("show_career_entry", career_entry_id=career_entry_id))

    return render_template(
        "make-career-entry.html",
        is_edit=True,
        career_entry_id=career_entry_id,
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/delete/career-entry/<int:career_entry_id>")
@admin_only
@login_required
def delete_career_entry(career_entry_id):
    career_entry_to_delete = db.get_or_404(Career, career_entry_id)
    db.session.delete(career_entry_to_delete)
    db.session.commit()
    return redirect(url_for('career'))

#----------------------------------------------------------------------------------------------------------------------#

#--------------------------------STUDIES-------------------------------------------------------------------------------#

@app.route("/studies")
def studies():
    result = db.session.execute(db.select(Studies))
    studies_entries = result.scalars().all()
    return render_template(
        "studies.html",
        studies_entries=studies_entries,
        logged_in=current_user.is_authenticated
    )

@app.route("/studies/<int:studies_entry_id>")
def show_studies_entry(studies_entry_id):

    selected_studies_entry = db.get_or_404(Studies, studies_entry_id)

    return render_template(
        "studies_entry.html",
        studies_entry=selected_studies_entry,
        logged_in = current_user.is_authenticated)

@app.route("/new-studies-entry", methods=["GET", "POST"])
@admin_only
@login_required
def add_new_studies_entry():
    form = StudiesEntryForm()

    if form.validate_on_submit():

        new_studies_entry = Studies(
            university = form.university.data,
            faculty = form.faculty.data,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            grade = form.grade.data,
            img_url = form.img_url.data,
        )

        db.session.add(new_studies_entry)
        db.session.commit()

        return redirect(url_for("studies"))

    return render_template(
        "make-studies-entry.html",
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/edit-studies-entry/<int:studies_entry_id>", methods=["GET", "POST"])
@admin_only
@login_required
def edit_studies_entry(studies_entry_id):
    selected_studies_entry = db.get_or_404(Studies, studies_entry_id)

    form = StudiesEntryForm(
        university = selected_studies_entry.university,
        faculty = selected_studies_entry.faculty,
        start_date = selected_studies_entry.start_date,
        end_date = selected_studies_entry.end_date,
        grade = selected_studies_entry.grade,
        img_url = selected_studies_entry.img_url,
    )

    if form.validate_on_submit():

        selected_studies_entry.university = form.university.data
        selected_studies_entry.faculty = form.faculty.data
        selected_studies_entry.start_date = form.start_date.data
        selected_studies_entry.end_date = form.end_date.data
        selected_studies_entry.grade = form.grade.data
        selected_studies_entry.img_url = form.img_url.data
        db.session.commit()

        return redirect(url_for("show_studies_entry", studies_entry_id=studies_entry_id))

    return render_template(
        "make-studies-entry.html",
        is_edit=True,
        studies_entry_id=studies_entry_id,
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/delete/studies/<int:studies_entry_id>")
@admin_only
@login_required
def delete_studies_entry(studies_entry_id):
    studies_entry_to_delete = db.get_or_404(Studies, studies_entry_id)
    db.session.delete(studies_entry_to_delete)
    db.session.commit()
    return redirect(url_for('studies'))

#----------------------------------------------------------------------------------------------------------------------#

#--------------------------------PROJECTS------------------------------------------------------------------------------#

@app.route("/projects")
def projects():
    result = db.session.execute(db.select(Projects))
    projects_entries = result.scalars().all()
    return render_template(
        "projects.html",
        projects_entries=projects_entries,
        logged_in=current_user.is_authenticated
    )

@app.route("/projects/<int:projects_entry_id>", methods=["GET", "POST"])
def show_projects_entry(projects_entry_id):

    selected_projects_entry = db.get_or_404(Projects, projects_entry_id)

    form = StepForm()

    if form.validate_on_submit():

        new_step = ProjectStep(
            name = form.name.data,
            completed = False,
            project = selected_projects_entry,
        )

        db.session.add(new_step)
        db.session.commit()

        return redirect(url_for('show_projects_entry', projects_entry_id=projects_entry_id))


    return render_template(
        "projects_entry.html",
        form=form,
        projects_entry=selected_projects_entry,
        logged_in = current_user.is_authenticated
    )

@app.route("/update-progress/step/<int:step_id>", methods=["POST"])
@admin_only
@login_required
def update_progress(step_id):

    # Get the project entry by ID

    selected_step = db.get_or_404(ProjectStep, step_id)

    selected_step.completed = request.form.get("completed")

    selected_projects_entry = db.get_or_404(Projects, selected_step.project_id)

    # Update the progress_level value

    completed_steps = 0

    for step in selected_projects_entry.steps:

        if step.completed:
            completed_steps += 1

    selected_step.progress = completed_steps / len(selected_projects_entry.steps)


    return redirect(url_for("show_projects_entry", projects_entry_id=selected_step.project_id))

@app.route("/new-projects-entry", methods=["GET", "POST"])
@admin_only
@login_required
def add_new_projects_entry():
    form = ProjectsEntryForm()

    if form.validate_on_submit():

        new_projects_entry = Projects(
            name = form.name.data,
            progress_level = form.progress_level.data,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            body = form.body.data,
            img_url = form.img_url.data,
        )

        db.session.add(new_projects_entry)
        db.session.commit()

        return redirect(url_for("projects"))

    return render_template(
        "make-projects-entry.html",
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/edit-projects-entry/<int:projects_entry_id>", methods=["GET", "POST"])
@admin_only
@login_required
def edit_projects_entry(projects_entry_id):
    selected_projects_entry = db.get_or_404(Projects, projects_entry_id)

    form = ProjectsEntryForm(
        name = selected_projects_entry.name,
        progress_level = selected_projects_entry.progress_level,
        start_date = selected_projects_entry.start_date,
        end_date = selected_projects_entry.end_date,
        body = selected_projects_entry.body,
        img_url = selected_projects_entry.img_url,
    )

    if form.validate_on_submit():

        selected_projects_entry.name = form.name.data
        selected_projects_entry.progress_level = form.progress_level.data
        selected_projects_entry.start_date = form.start_date.data
        selected_projects_entry.end_date = form.end_date.data
        selected_projects_entry.body = form.body.data
        selected_projects_entry.img_url = form.img_url.data
        db.session.commit()

        return redirect(url_for("show_projects_entry", projects_entry_id=projects_entry_id))

    return render_template(
        "make-projects-entry.html",
        is_edit=True,
        projects_entry_id=projects_entry_id,
        form=form,
        logged_in = current_user.is_authenticated
    )

@app.route("/delete/projects/<int:projects_entry_id>")
@admin_only
@login_required
def delete_projects_entry(projects_entry_id):
    projects_entry_to_delete = db.get_or_404(Projects, projects_entry_id)
    db.session.delete(projects_entry_to_delete)
    db.session.commit()
    return redirect(url_for('projects'))

#----------------------------------------------------------------------------------------------------------------------#

#--------------------------------RECOMMENDATIONS-----------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#

#--------------------------------ABOUT & CONTACT ROUTES----------------------------------------------------------------#

@app.route("/about")
def about():
    return render_template("about.html", logged_in = current_user.is_authenticated)

@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in = current_user.is_authenticated)

#----------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
