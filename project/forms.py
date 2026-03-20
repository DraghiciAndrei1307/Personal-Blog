
"""A collection of Flask forms used throughout the project"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):

    """Create Post Form"""

    title = StringField(
        "Blog Post Title",
        validators=[DataRequired()]
    )
    subtitle = StringField(
        "Subtitle",
        validators=[DataRequired()]
    )
    img_url = StringField(
        "Blog Image URL",
        validators=[DataRequired(), URL()]
    )
    body = CKEditorField(
        "Blog Content",
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):

    """Register Form"""

    email = StringField(
        "Email",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    name = StringField(
        "Name",
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):

    """Login Form"""

    email = StringField(
        "Email",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):

    """Comment Form"""

    body = CKEditorField(
        "Comment",
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Comment")


class CareerEntryForm(FlaskForm):

    """Career Entry Form"""

    organization_name = StringField(
        "Organization Name",
        validators=[DataRequired()]
    )
    role = StringField(
        "Domain Name",
        validators=[DataRequired()]
    )
    start_date = StringField(
        "Start Date",
        validators=[DataRequired()]
    )
    end_date = StringField(
        "End Date",
        validators=[DataRequired()]
    )
    activity = CKEditorField(
        "Activity",
        validators=[DataRequired()]
    )
    img_url = StringField(
        "Organization Image URL",
        validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit")


class StudiesEntryForm(FlaskForm):

    """Studies Entry Form"""

    university = StringField(
        "Organization Name",
        validators=[DataRequired()]
    )
    faculty = StringField(
        "Domain Name",
        validators=[DataRequired()]
    )
    start_date = StringField(
        "Start Date",
        validators=[DataRequired()]
    )
    end_date = StringField(
        "End Date",
        validators=[DataRequired()]
    )
    grade = StringField(
        "Grade",
        validators=[DataRequired()]
    )
    img_url = StringField(
        "Organization Image URL",
        validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit")


class ProjectsEntryForm(FlaskForm):

    """Projects Entry Form"""

    name = StringField(
        "Project Name",
        validators=[DataRequired()]
    )
    start_date = StringField(
        "Start Date",
        validators=[DataRequired()]
    )
    end_date = StringField(
        "End Date",
        validators=[DataRequired()]
    )
    body = CKEditorField(
        "Description",
        validators=[DataRequired()]
    )
    img_url = StringField(
        "Project Image URL",
        validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit")


class StepForm(FlaskForm):

    """Step Form"""

    name = StringField(
        "Step Name",
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Step")
