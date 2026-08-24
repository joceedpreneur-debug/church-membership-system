import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "temporary-development-key"
)


# Get database URL from Render
database_url = os.environ.get("DATABASE_URL")

# Convert old postgres:// format to postgresql://
if database_url:
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MEMBER DATABASE TABLE
# =========================

class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    gender = db.Column(
        db.String(20)
    )

    age = db.Column(
        db.Integer
    )

    phone = db.Column(
        db.String(30)
    )

    department = db.Column(
        db.String(100)
    )

    date_joined = db.Column(
        db.String(30)
    )

    status = db.Column(
        db.String(30),
        default="Active"
    )


# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():
    db.create_all()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template(
        "login.html"
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    total_members = Member.query.count()

    active_members = Member.query.filter_by(
        status="Active"
    ).count()

    return render_template(
        "dashboard.html",
        total_members=total_members,
        active_members=active_members
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )
