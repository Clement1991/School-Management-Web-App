import os
from cs50 import SQL
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    get_flashed_messages,
)
from werkzeug.security import check_password_hash, generate_password_hash

# Authenticates user email
from validator_collection import validators

# Secures file (photo) names during uploads
from werkzeug.utils import secure_filename

#  Converts photos into hash content
import hashlib

# Provides a list of all nationalities or countries.
import pycountry

# Import app (application name) from app.py
from app import app

# Configure Flask app to specify the photo upload folder.
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static", "photos")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school.db")

# Create Global variables GENDER, STATUS, nationalities
GENDER = ["M", "F"]

STATUS = ["Student", "Teaching staff", "Non-teaching staff"]

# Get a list of nationalities from pycountry
nationalities = [country.name for country in pycountry.countries]


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # Get a list of nationalities from pycountry
    nationalities = [country.name for country in pycountry.countries]

    programs = db.execute("SELECT * FROM programs")
    departments = db.execute("SELECT * FROM departments")

    if request.method == "POST":
        status = request.form.get("status")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        if len(month) < 2:
            month = "0" + str(month)
        if len(day) < 2:
            day = "0" + str(day)
        dob = str(year) + "-" + str(month) + "-" + str(day)
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        # GET PHOTO: Initialize photo name and photo hashes to None
        photo_name = None
        photo_hash = None

        # Request for photo
        if "photo" in request.files:
            photo = request.files["photo"]

            # If photo is present or uploaded
            if photo.filename != "":
                # Check if the file has a valid extension
                allowed_extensions = {"png", "jpg", "jpeg", "gif"}
                photo_extension = (
                    secure_filename(photo.filename).rsplit(".", 1)[1].lower()
                    if "." in photo.filename
                    else ""
                )

                if photo_extension not in allowed_extensions:
                    flash(
                        "Invalid file extension. Allowed extensions: 'png', 'jpg', 'jpeg', 'gif'.",
                        category="danger",
                    )

                else:
                    # Generate a unique filename using the hash of the photo content and its original extension
                    photo_hash = hashlib.md5(photo.read()).hexdigest()
                    photo_name = f"{first_name}_{last_name}_{photo_hash}.{photo_extension}"

                    # Save the file to the 'photos' folder in the static directory
                    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_name)

                    # Reset the file pointer before saving
                    photo.seek(0)
                    photo.save(photo_path)

        try:
            email = validators.email(email)
        except:
            flash("Invalid email!!!! Please enter a valid email address!", "danger")
            return render_template(
                "register.html",
                status=STATUS,
                nationalities=nationalities,
                gender=GENDER,
                programs=programs,
                departments=departments,
            )

        if not status or status not in STATUS:
            flash("Please select status!", category="danger")
        elif len(first_name) < 2 or len(last_name) < 2:
            flash(
                "First name and Last name must have more than 1 character.",
                category="danger",
            )
        elif not year or not month or not day:
            flash("Please enter all fields for date of birth!", category="danger")
        elif password != confirmation:
            flash("Passwords don't match.", category="danger")
        elif len(password) < 3:
            flash("Password must have at least 3 characters.", category="danger")
        elif not gender or gender not in GENDER:
            flash("Please enter a valid gender!", category="danger")
        elif not nationality:
            flash("Please enter nationality!", category="danger")
        elif not phone:
            flash("Please enter phone number!", category="danger")
        elif not address:
            flash("Please enter address!", category="danger")

        else:
            if status == "Student":
                program = request.form.get("program")
                school = request.form.get("school")

                if not program:
                    flash("Please enter program!", category="danger")

                elif not school:
                    flash("Please enter previous school attended!", category="danger")

                else:
                    # Check if student email already exists in the database
                    rows = db.execute("SELECT * FROM students WHERE email = ?", email)
                    other = db.execute("SELECT * FROM staff WHERE email = ?", email)

                    if len(rows) > 0 or len(other) > 0:
                        flash(
                            "Email already exists! Enter a different email address.",
                            "danger",
                        )
                    else:
                        # Get program id
                        program_id = db.execute(
                            "SELECT id FROM programs WHERE name =?", program
                        )[0]["id"]

                        hashed_password = generate_password_hash(password)

                        db.execute(
                            "INSERT INTO students (photo, photo_hash, first_name, last_name, date_of_birth, gender, nationality, previous_school, password, email, phone, address, program_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            photo_name,
                            photo_hash,
                            first_name,
                            last_name,
                            dob,
                            gender,
                            nationality,
                            school,
                            hashed_password,
                            email,
                            phone,
                            address,
                            program_id,
                        )

                        flash("Success!!!! Student account created.", "success")
                        return redirect("/")
            else:
                # Check if staff email already exists in the database
                rows = db.execute("SELECT * FROM staff WHERE email = ?", email)
                other = db.execute("SELECT * FROM students WHERE email = ?", email)

                if len(rows) > 0 or len(other) > 0:
                    flash(
                        "Email already exists! Enter a different email address!!!",
                        "danger",
                    )
                else:
                    department = request.form.get("department")

                    if not department:
                        flash("Please enter department!", "danger")
                    else:
                        department_id = db.execute(
                            "SELECT id FROM departments WHERE name = ?", department
                        )[0]["id"]

                        hashed_password = generate_password_hash(password)

                        db.execute(
                            "INSERT INTO staff (photo, photo_hash, first_name, last_name, date_of_birth, gender, nationality, password, email, phone, address, department_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            photo_name,
                            photo_hash,
                            first_name,
                            last_name,
                            dob,
                            gender,
                            nationality,
                            hashed_password,
                            email,
                            phone,
                            address,
                            department_id,
                            status,
                        )

                        flash("Staff account created!!!", "success")
                        return redirect("/")

        return render_template(
            "register.html",
            status=STATUS,
            gender=GENDER,
            nationalities=nationalities,
            programs=programs,
            departments=departments,
        )

    else:
        return render_template(
            "register.html",
            nationalities=nationalities,
            gender=GENDER,
            status=STATUS,
            programs=programs,
            departments=departments,
        )
