import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = "myapp"

# Import your route blueprints
from register import app
from login import app
from students_edt import app
from teaching import app
from teachers_edit import app
from deregister import app
from staff_edit import app

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Flask app to specify the photo upload folder.
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static", "photos")

# Photo file extensions allowed
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school.db")

# Create Global variables
GENDER = ["M", "F"]

STATUS = ["Student", "Teaching staff", "Non-teaching staff"]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def dashboard():
    user_id = session["user_id"]
    status = session["status"]

    if status == "Student":
        profile = db.execute("SELECT * FROM students WHERE id = ?", user_id)
    else:
        profile = db.execute("SELECT * FROM staff WHERE id = ?", user_id)

    return render_template("dashboard.html", profile=profile)


@app.route("/logout")
def logout():
    user_id = session["user_id"]
    status = session["status"]

    if status == "Student":
        profile = db.execute("SELECT * FROM students WHERE id = ?", user_id)
        email = profile[0]["email"]
        password = profile[0]["password"]

        db.execute(
            "INSERT INTO student_logs (type, old_email, new_email, old_password, new_password) VALUES (?, ?, ?, ?, ?)",
            "logout",
            "NULL",
            email,
            "NULL",
            password,
        )
    else:
        profile = db.execute("SELECT * FROM staff WHERE id = ?", user_id)
        email = profile[0]["email"]
        password = profile[0]["password"]
        db.execute(
            "INSERT INTO staff_logs (type, old_email, new_email, old_password, new_password) VALUES (?, ?, ?, ?, ?)",
            "logout",
            "NULL",
            email,
            "NULL",
            password,
        )

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/students")
@login_required
def students():
    user_id = session["user_id"]
    profile = db.execute("SELECT * FROM students WHERE id = ?", user_id)
    program_id = profile[0]["program_id"]
    program = db.execute("SELECT name FROM programs WHERE id = ?", program_id)[0][
        "name"
    ]
    department = db.execute(
        "SELECT name FROM departments WHERE id = (SELECT department_id FROM programs WHERE id = ?)",
        program_id,
    )[0]["name"]

    courses = db.execute(
        "SELECT name, year FROM courses JOIN outlines ON courses.id = outlines.course_id WHERE program_id = ?",
        program_id,
    )

    return render_template(
        "students.html",
        students=profile,
        program=program,
        department=department,
        courses=courses,
    )


@app.route("/teachers")
@login_required
def teachers():
    user_id = session["user_id"]

    profile = db.execute("SELECT * FROM staff WHERE id = ?", user_id)
    department_id = profile[0]["department_id"]
    department = db.execute("SELECT name FROM departments WHERE id = ?", department_id)[
        0
    ]["name"]
    courses = db.execute(
        "SELECT * FROM courses WHERE id IN (SELECT course_id FROM classes WHERE staff_id = ?)",
        user_id,
    )

    return render_template(
        "teachers.html", staff=profile, department=department, courses=courses
    )


@app.route("/staff")
@login_required
def staff():
    user_id = session["user_id"]

    profile = db.execute("SELECT * FROM staff WHERE id = ?", user_id)
    department_id = profile[0]["department_id"]
    department = db.execute("SELECT name FROM departments WHERE id = ?", department_id)[
        0
    ]["name"]

    return render_template("staff.html", staff=profile, department=department)


@app.route("/courses")
@login_required
def courses():
    user_id = session["user_id"]
    profile = db.execute("SELECT * FROM students WHERE id = ?", user_id)
    program_id = profile[0]["program_id"]
    courses = db.execute(
        "SELECT name, year FROM courses JOIN outlines ON courses.id = outlines.course_id WHERE program_id = ?",
        program_id,
    )

    return render_template("courses.html", courses=courses)


@app.route("/remove", methods=["POST"])
def remove():
    # Get user id from database stored in session
    user_id = session["user_id"]

    # Get user id from form
    id = request.form.get("id")

    # If id exists
    if id:
        db.execute(
            "DELETE FROM classes WHERE course_id = ? AND staff_id = ?", id, user_id
        )
        flash("Course successfully removed ", category="success")
    else:
        flash("Failed to remove the class", "danger")
    return redirect("/teachers")


@app.route("/programs")
@login_required
def programs():
    programs = db.execute("SELECT * FROM programs")
    return render_template("programs.html", programs=programs)


@app.route("/departments")
@login_required
def departments():
    departments = db.execute("SELECT * FROM departments")
    return render_template("departments.html", departments=departments)
