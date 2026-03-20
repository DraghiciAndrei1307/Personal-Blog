
"""Models used in the project"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class Base(DeclarativeBase):

    """Base Model"""


db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model): # UserMixin contains some special attributes
                                 # and methods required for the log in
    """User Model"""
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")

# BlogPost model to create a table for all blog posts created by the admin users

class BlogPost(db.Model):

    """Blog Post Model"""

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

    """Comment Model"""

    __tablename__ = "comment_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)

    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts_table.id"))
    post = relationship("BlogPost", back_populates="comments")

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("user_table.id"))
    author = relationship("User", back_populates="comments")


class Career(db.Model):

    """Career Model"""

    __tablename__ = "career_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(250), nullable=False)
    role: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[str] = mapped_column(String(250), nullable=False)
    end_date: Mapped[str] = mapped_column(String(250), nullable=False)
    activity: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Studies(db.Model):

    """Studies Model"""

    __tablename__ = "studies_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university: Mapped[str] = mapped_column(String(250), nullable=False)
    faculty: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[str] = mapped_column(String(250), nullable=False)
    end_date: Mapped[str] = mapped_column(String(250), nullable=False)
    grade: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Projects(db.Model):

    """Projects Model"""

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

    """Project Step Model"""

    __tablename__ = "project_steps_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    project_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("projects_table.id"))
    project = relationship("Projects", back_populates="steps")
