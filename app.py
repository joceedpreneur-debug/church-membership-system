import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "temporary-development-key"
)


database_url = os.environ.get("DATABASE_URL")


if database_url:

    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )


app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# ==========================================
# MEMBER MODEL
# ==========================================

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


# ==========================================
# ATTENDANCE MODEL
# ==========================================

class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.String(30),
        nullable=False
    )

    service_type = db.Column(
        db.String(50),
        nullable=False
    )

    attendance_status = db.Column(
        db.String(20),
        nullable=False
    )


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

with app.app_context():

    db.create_all()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template(
        "login.html"
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    total_members = Member.query.count()

    active_members = Member.query.filter_by(
        status="Active"
    ).count()


    total_attendance = Attendance.query.count()


    present_attendance = Attendance.query.filter_by(
        attendance_status="Present"
    ).count()


    if total_attendance > 0:

        attendance_percentage = round(
            (
                present_attendance /
                total_attendance
            ) * 100,
            1
        )

    else:

        attendance_percentage = 0


    return render_template(
        "dashboard.html",
        total_members=total_members,
        active_members=active_members,
        attendance=attendance_percentage
    )


# ==========================================
# ADD MEMBER PAGE
# ==========================================

@app.route("/add-member")
def add_member():

    return render_template(
        "add_member.html"
    )


# ==========================================
# SAVE MEMBER
# ==========================================

@app.route(
    "/add-member",
    methods=["POST"]
)

def save_member():

    full_name = request.form.get(
        "full_name"
    )

    gender = request.form.get(
        "gender"
    )

    age = request.form.get(
        "age"
    )

    phone = request.form.get(
        "phone"
    )

    department = request.form.get(
        "department"
    )

    date_joined = request.form.get(
        "date_joined"
    )

    status = request.form.get(
        "status"
    )


    if age:

        age = int(age)

    else:

        age = None


    new_member = Member(

        full_name=full_name,

        gender=gender,

        age=age,

        phone=phone,

        department=department,

        date_joined=date_joined,

        status=status

    )


    db.session.add(
        new_member
    )

    db.session.commit()


    return redirect(
        url_for("members")
    )


# ==========================================
# VIEW MEMBERS
# ==========================================

@app.route("/members")
def members():

    all_members = Member.query.order_by(
        Member.id.desc()
    ).all()


    return render_template(
        "members.html",
        members=all_members
    )


# ==========================================
# ATTENDANCE PAGE
# ==========================================

@app.route("/attendance")
def attendance():

    all_members = Member.query.filter_by(
        status="Active"
    ).order_by(
        Member.full_name
    ).all()


    return render_template(
        "attendance.html",
        members=all_members
    )


# ==========================================
# SAVE ATTENDANCE
# ==========================================

@app.route(
    "/attendance",
    methods=["POST"]
)

def save_attendance():

    member_id = request.form.get(
        "member_id"
    )

    attendance_date = request.form.get(
        "attendance_date"
    )

    service_type = request.form.get(
        "service_type"
    )

    attendance_status = request.form.get(
        "attendance_status"
    )


    new_attendance = Attendance(

        member_id=member_id,

        attendance_date=attendance_date,

        service_type=service_type,

        attendance_status=attendance_status

    )


    db.session.add(
        new_attendance
    )

    db.session.commit()


    return redirect(
        url_for("attendance_history")
    )


# ==========================================
# ATTENDANCE HISTORY
# ==========================================

@app.route("/attendance-history")
def attendance_history():

    records = db.session.query(
        Attendance,
        Member
    ).join(
        Member,
        Attendance.member_id == Member.id
    ).order_by(
        Attendance.id.desc()
    ).all()


    return render_template(
        "attendance_history.html",
        records=records
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
