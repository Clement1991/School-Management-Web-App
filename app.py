import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Authenticates user email
from validator_collection import validators

# Secures file (photo) names during uploads
from werkzeug.utils import secure_filename

#  Converts photos into hash content
import hashlib

# Provides a list of all nationalities or countries.
import pycountry

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = "myapp"


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

nationalities = [country.name for country in pycountry.countries]

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

@app.route("/deregister", methods=["POST"])
def deregister():
    user_id = session["user_id"]
    status = session["status"]

    id = request.form.get("id")

    if id:
        if status == "Student":
            db.execute("DELETE FROM students WHERE id = ?", user_id)
        else:
            db.execute("DELETE FROM staff WHERE id = ?", user_id)

    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        status = request.form.get("status")
        email = request.form.get("email").lower()
        password = request.form.get("password")

        if not status or status not in STATUS:
            flash("Please select status!", "danger")
        elif not email:
            flash("Please enter email!", "danger")
        elif not password:
            flash("Please enter password!", "danger")
        else:
            if status == "Student":
                rows = db.execute("SELECT * FROM students WHERE email = ?", email)

                if len(rows) != 1:
                    flash("Account does not exist! Please enter a new email.", "danger")
                elif not check_password_hash(rows[0]["password"], password):
                    flash("Invalid password! Please enter a correct password.", "danger")
                else:
                    db.execute(
                        "INSERT INTO student_logs (type, old_email, new_email, old_password, new_password) VALUES (?, ?, ?, ?, ?)",
                        "login",
                        "NULL",
                        email,
                        "NULL",
                        generate_password_hash(password),
                    )

                    flash("Logged in succefully!", "success")

                    # Remember which user has logged in
                    session["user_id"] = rows[0]["id"]

                    # Remember user status
                    session["status"] = "Student"

                    # Handle successful login attempts
                    return redirect("/")

            elif status == "Teaching staff":
                rows = db.execute("SELECT * FROM staff WHERE email = ? AND status = ?", email, "Teaching staff")

                if len(rows) != 1:
                    flash("Account does not exist! Please enter a new email.", "danger")
                elif not check_password_hash(rows[0]["password"], password):
                    flash("Invalid password! Please enter a correct password.", "danger")
                else:
                    db.execute(
                        "INSERT INTO staff_logs (type, old_email, new_email, old_password, new_password) VALUES (?, ?, ?, ?, ?)",
                        "login",
                        "NULL",
                        email,
                        "NULL",
                        generate_password_hash(password),
                    )

                    flash("Logged in succefully!", "success")

                    # Remember which user has logged in
                    session["user_id"] = rows[0]["id"]

                    # Remember user status
                    session["status"] = "Teaching staff"

                    # Handle successful login attempts
                    return redirect("/")

            else:
                rows = db.execute("SELECT * FROM staff WHERE email = ? AND status = ?", email, "Non-teaching staff")

                # If email already exists in the database
                if len(rows) != 1:
                    flash("Account does not exist! Please enter a new email.", "danger")

                # Verify password from database
                elif not check_password_hash(rows[0]["password"], password):
                    flash("Invalid password! Please enter a correct password.", "danger")
                else:
                    db.execute(
                        "INSERT INTO staff_logs (type, old_email, new_email, old_password, new_password) VALUES (?, ?, ?, ?, ?)",
                        "login",
                        "NULL",
                        email,
                        "NULL",
                        generate_password_hash(password),
                    )

                    flash("Logged in succefully!", "success")

                    # Remember which user has logged in
                    session["user_id"] = rows[0]["id"]

                    # Remember status of user
                    session["status"] = "Non-teaching staff"

                    # Handle successful login attempts
                    return redirect("/")

            # Handle unsuccessful login attempts
            return render_template("login.html", status=STATUS)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", status=STATUS)


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
        photoname = None

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

                # Generate a unique filename using the hash of the photo content and its original extension
                photo_content = photo.read()
                photo_hash = hashlib.md5(photo_content).hexdigest()
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

                    if len(rows) > 0:
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
                            "INSERT INTO students (photo, first_name, last_name, date_of_birth, gender, nationality, previous_school, password, email, phone, address, program_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            photoname,
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

                if len(rows) > 0:
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
                            "INSERT INTO staff (photo, first_name, last_name, date_of_birth, gender, nationality, password, email, phone, address, department_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            photoname,
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

@app.route("/staff_edit", methods=["GET", "POST"])
@login_required
def staff_edit():
    user_id = session["user_id"]
    staff = db.execute("SELECT * FROM staff WHERE id = ?", user_id)

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        try:
            if validators.email(email):
                pass
        except Exception as e:
            flash("Please enter a valid email address!")
            return redirect("/staff_edit")

        # Check if the 'changePassword' checkbox is selected
        change_password = request.form.get("changePassword")
        if change_password:
            old_password = request.form.get("oldPassword")
            new_password = request.form.get("newPassword")
            confirmation = request.form.get("confirmPassword")

            # Validate old password
            if not check_password_hash(staff[0]["password"], old_password):
                flash("Incorrect old password. Please try again.")
                return redirect("/staff_edit")

            if old_password == new_password:
                flash("Old and new passwords are the same. Please try again.")
                return redirect("/staff_edit")

            # Check if new password and confirmation match
            if new_password != confirmation:
                flash("New password and confirmation do not match. Please try again.")
                return redirect("/staff_edit")

            # Update the password in the database
            hashed_password = generate_password_hash(new_password)
            db.execute(
                "UPDATE staff SET password = ? WHERE id = ?", hashed_password, user_id
            )

            # Forget any user_id
            session.clear()

        # Initialize photo_name and photo_hash to None
        photo_name = None
        photo_hash = None

        # Request for a new photo
        if "photo" in request.files:
            photo = request.files["photo"]

            # Check if a new photo is provided
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
                        "Invalid file extension. Allowed extensions: 'png', 'jpg', 'jpeg', 'gif'."
                    )
                    return redirect("/staff_edit")

                # Generate a unique filename using the hash of the photo content and its original extension
                photo_hash = hashlib.md5(photo.read()).hexdigest()
                photo_name = f"{first_name}_{last_name}_{photo_hash}.{photo_extension}"

                # Retrieve the current photo filename and hash from the database
                current_photo = staff[0]["photo"]
                current_photo_hash = staff[0]["photo_hash"]

                # Save the new photo only if the hashes are different
                if current_photo_hash != photo_hash:
                    # Save the file to the 'photos' folder in the static directory
                    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_name)

                    # Reset the file pointer before saving
                    photo.seek(0)
                    photo.save(photo_path)

                    # Update the database with the current photo and photo_hash
                    db.execute(
                        "UPDATE staff SET photo = ? WHERE id = ?", photo_name, user_id
                    )
                    db.execute(
                        "UPDATE staff SET photo_hash = ? WHERE id = ?",
                        photo_hash,
                        user_id,
                    )

                    # Remove the old photo if it exists
                    if current_photo:
                        old_photo_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], current_photo
                        )
                        if os.path.exists(old_photo_path):
                            os.remove(old_photo_path)

        # Update staff information if changes have been made
        if first_name != staff[0]["first_name"]:
            db.execute(
                "UPDATE staff SET first_name = ? WHERE id = ?", first_name, user_id
            )
        if last_name != staff[0]["last_name"]:
            db.execute(
                "UPDATE staff SET last_name = ? WHERE id = ?", last_name, user_id
            )
        if date_of_birth != staff[0]["date_of_birth"]:
            db.execute(
                "UPDATE staff SET date_of_birth = ? WHERE id = ?",
                date_of_birth,
                user_id,
            )
        if gender != staff[0]["gender"]:
            db.execute("UPDATE staff SET gender = ? WHERE id = ?", gender, user_id)
        if nationality != staff[0]["nationality"]:
            db.execute(
                "UPDATE staff SET nationality = ? WHERE id = ?", nationality, user_id
            )
        if email != staff[0]["email"]:
            db.execute("UPDATE staff SET email = ? WHERE id = ?", email, user_id)
        if phone != staff[0]["phone"]:
            db.execute("UPDATE staff SET phone = ? WHERE id = ?", phone, user_id)
        if address != staff[0]["address"]:
            db.execute("UPDATE staff SET address = ? WHERE id = ?", address, user_id)

        flash("Profile updated successfully!", "success")
        return redirect(
            "/staff"
        )  # Redirect to the dashboard or another appropriate route

    else:
        nationalities = [country.name for country in pycountry.countries]
        return render_template(
            "staff_edit.html", staff=staff, gender=GENDER, nationalities=nationalities
        )

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    user_id = session["user_id"]
    students = db.execute("SELECT * FROM students WHERE id = ?", user_id)
    programs = db.execute("SELECT * FROM programs")

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        school = request.form.get("school")
        program = request.form.get("program")

        # validate email
        try:
            email = validators.email(email)
        except:
            flash("Please enter a valid email address!", "danger")
            return redirect("/edit")

        if len(first_name) < 2 or len(last_name) < 2:
            flash(
                "First name and Last name must have more than 1 character.",
                category="danger",
            )
            return redirect("/edit")
        if not date_of_birth:
            flash("Please enter date of birth!", category="danger")
            return redirect("/edit")
        if not gender or gender not in GENDER:
            flash("Please enter a valid gender!", category="danger")
            return redirect("/edit")
        if not nationality:
            flash("Please enter nationality!", category="danger")
            return redirect("/edit")
        if not phone:
            flash("Please enter phone number!", category="danger")
            return redirect("/edit")
        if not address:
            flash("Please enter address!", category="danger")
            return redirect("/edit")
        if not program:
            flash("Please enter program!", category="danger")
            return redirect("/edit")
        if not school:
            flash("Please enter previous school attended!", category="danger")
            return redirect("/edit")

        # Get student's information
        student = db.execute("SELECT * FROM students WHERE id = ?", user_id)
        program_id = db.execute("SELECT id FROM programs WHERE name = ?", program)[0][
            "id"
        ]

        # Update student's information if changes have been made
        if first_name != student[0]["first_name"]:
            db.execute(
                "UPDATE students SET first_name = ? WHERE id = ?", first_name, user_id
            )
        if last_name != student[0]["last_name"]:
            db.execute(
                "UPDATE students SET last_name = ? WHERE id = ?", last_name, user_id
            )
        if date_of_birth != student[0]["date_of_birth"]:
            db.execute(
                "UPDATE students SET date_of_birth = ? WHERE id = ?",
                date_of_birth,
                user_id,
            )
        if gender != student[0]["gender"]:
            db.execute("UPDATE students SET gender = ? WHERE id = ?", gender, user_id)
        if nationality != student[0]["nationality"]:
            db.execute(
                "UPDATE students SET nationality = ? WHERE id = ?", nationality, user_id
            )
        if school != student[0]["previous_school"]:
            db.execute(
                "UPDATE students SET previous_school = ? WHERE id = ?", school, user_id
            )
        if email != student[0]["email"]:
            db.execute("UPDATE students SET email = ? WHERE id = ?", email, user_id)
        if phone != student[0]["phone"]:
            db.execute("UPDATE students SET phone = ? WHERE id = ?", phone, user_id)
        if address != student[0]["address"]:
            db.execute("UPDATE students SET address = ? WHERE id = ?", address, user_id)
        if program_id != student[0]["program_id"]:
            db.execute(
                "UPDATE students SET program_id = ? WHERE id = ?", program_id, user_id
            )

        # Check if the 'changePassword' checkbox is selected
        change_password = request.form.get("changePassword")
        if change_password:
            old_password = request.form.get("oldPassword")
            new_password = request.form.get("newPassword")
            confirmation = request.form.get("confirmPassword")

            # Validate old password
            if not check_password_hash(student[0]["password"], old_password):
                flash("Incorrect old password. Please try again.", "danger")
                return redirect("/edit")

            # Check if new password and confirmation match
            if old_password == new_password:
                flash("Old and new passwords are the same", "danger")
                return redirect("/edit")

            # Check if new password and confirmation match
            if new_password != confirmation:
                flash(
                    "New password and confirmation do not match. Please try again.",
                    "danger",
                )
                return redirect("/edit")

            # Update the password in the database
            hashed_password = generate_password_hash(new_password)
            db.execute(
                "UPDATE students SET password = ? WHERE id = ?",
                hashed_password,
                user_id,
            )
            flash("Password updated successfully", "success")

            # Forget any user_id
            session.clear()

        # Retrieve the current photo filename and hash from the database
        current_photo = student[0]["photo"]
        current_photo_hash = student[0]["photo_hash"]

        # Initialize photo_name and photo_hash to None
        photo_name = None
        #photo_hash = None

        # Request for a new photo
        if "photo" in request.files:
            photo = request.files["photo"]

            # Check if a new photo is provided
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
                        "danger",
                    )
                    return redirect("/edit")

                # Generate a unique filename using the hash of the photo content and its original extension
                photo_hash = hashlib.md5(photo.read()).hexdigest()
                photo_name = f"{first_name}_{last_name}_{photo_hash}.{photo_extension}"

                # Save the new photo only if the hashes are different
                if current_photo_hash != photo_hash:
                    # Save the file to the 'photos' folder in the static directory
                    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_name)

                    # Reset the file pointer before saving
                    photo.seek(0)
                    photo.save(photo_path)

                    # Update the database with the current photo
                    db.execute(
                        "UPDATE students SET photo = ? WHERE id = ?",
                        photo_name,
                        user_id,
                    )

                    # Remove the old photo if it exists
                    if current_photo:
                        old_photo_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], current_photo
                        )
                        if os.path.exists(old_photo_path):
                            os.remove(old_photo_path)

        flash("Profile updated successfully!", "success")
        return redirect("/students")

    else:
        return render_template(
            "edit.html",
            students=students,
            gender=GENDER,
            nationalities=nationalities,
            programs=programs,
        )


@app.route("/teachers_edit", methods=["GET", "POST"])
@login_required
def teachers_edit():
    user_id = session["user_id"]

    # Get student's information
    teachers = db.execute("SELECT * FROM staff WHERE id = ?", user_id)

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        try:
            email = validators.email(email)
        except:
            flash("Please enter a valid email address!", category="danger")
            return redirect("/teachers_edit")

        if len(first_name) < 2 or len(last_name) < 2:
            flash(
                "First name and Last name must have more than 1 character.",
                category="danger",
            )
            return redirect("/teachers_edit")
        if not date_of_birth:
            flash("Please enter all fields for date of birth!", category="danger")
            return redirect("/teachers_edit")
        if not gender or gender not in GENDER:
            flash("Please enter a valid gender!", category="danger")
            return redirect("/teachers_edit")
        if not nationality:
            flash("Please enter nationality!", category="danger")
            return redirect("/teachers_edit")
        if not phone:
            flash("Please enter phone number!", category="danger")
            return redirect("/teachers_edit")
        if not address:
            flash("Please enter address!", category="danger")
            return redirect("/teachers_edit")

        # Update staff information if changes have been made
        if first_name != teachers[0]["first_name"]:
            db.execute(
                "UPDATE staff SET first_name = ? WHERE id = ?", first_name, user_id
            )
        if last_name != teachers[0]["last_name"]:
            db.execute(
                "UPDATE staff SET last_name = ? WHERE id = ?", last_name, user_id
            )
        if date_of_birth != teachers[0]["date_of_birth"]:
            db.execute(
                "UPDATE staff SET date_of_birth = ? WHERE id = ?",
                date_of_birth,
                user_id,
            )
        if gender != teachers[0]["gender"]:
            db.execute("UPDATE staff SET gender = ? WHERE id = ?", gender, user_id)
        if nationality != teachers[0]["nationality"]:
            db.execute(
                "UPDATE staff SET nationality = ? WHERE id = ?", nationality, user_id
            )
        if email != teachers[0]["email"]:
            db.execute("UPDATE staff SET email = ? WHERE id = ?", email, user_id)
        if phone != teachers[0]["phone"]:
            db.execute("UPDATE staff SET phone = ? WHERE id = ?", phone, user_id)
        if address != teachers[0]["address"]:
            db.execute("UPDATE staff SET address = ? WHERE id = ?", address, user_id)

        # Check if the 'changePassword' checkbox is selected
        change_password = request.form.get("changePassword")
        if change_password:
            old_password = request.form.get("oldPassword")
            new_password = request.form.get("newPassword")
            confirmation = request.form.get("confirmPassword")

            # Validate old password
            if not check_password_hash(teachers[0]["password"], old_password):
                flash("Incorrect old password. Please try again.", category="danger")
                return redirect("/teachers_edit")

            # Check if new password and confirmation match
            if new_password != confirmation:
                flash("New password and confirmation do not match. Please try again.")
                return redirect("/teachers_edit")

            # Update the password in the database
            hashed_password = generate_password_hash(new_password)
            db.execute(
                "UPDATE staff SET password = ? WHERE id = ?", hashed_password, user_id
            )

            # Forget any user_id
            session.clear()

        # Retrieve the current photo filename and hash from the database
        current_photo = teachers[0]["photo"]
        current_photo_hash = teachers[0]["photo_hash"]

        # Initialize photo_name and photo_hash to None
        photo_name = None
        photo_hash = None

        # Request for a new photo
        if "photo" in request.files:
            photo = request.files["photo"]

            # Check if a new photo has been uploaded
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
                    return redirect("/teachers_edit")

                # Generate a unique filename using the hash of the photo content and its original extension
                photo_hash = hashlib.md5(photo.read()).hexdigest()
                photo_name = f"{first_name}_{last_name}_{photo_hash}.{photo_extension}"

                # Save the new photo only if the hashes are different
                if current_photo_hash != photo_hash:
                    # Save the file to the 'photos' folder in the static directory
                    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_name)

                    # Reset the file pointer before saving
                    photo.seek(0)
                    photo.save(photo_path)

                    # Update the database with the current photo and photo_hash
                    db.execute(
                        "UPDATE staff SET photo = ?, photo_hash = ? WHERE id = ?",
                        photo_name,
                        photo_hash,
                        user_id,
                    )

                    # Remove the old photo if it exists
                    if current_photo:
                        old_photo_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], current_photo
                        )
                        if os.path.exists(old_photo_path):
                            os.remove(old_photo_path)

        flash("Profile updated successfully!", category="success")
        return redirect("/teachers")

    else:
        return render_template(
            "teachers_edit.html",
            teachers=teachers,
            gender=GENDER,
            nationalities=nationalities,
        )


@app.route("/teaching", methods=["GET", "POST"])
@login_required
def teaching():
    user_id = session["user_id"]

    if request.method == "POST":
        courses = request.form.getlist("course")

        for course in courses:
            course_id = db.execute("SELECT id FROM courses WHERE name = ?", course)[0][
                "id"
            ]

            # Check if the record already exists in the 'classes' table
            existing_record = db.execute(
                "SELECT * FROM classes WHERE staff_id = ? AND course_id = ?",
                user_id,
                course_id,
            )

            if not existing_record:
                # Insert into the 'classes' table for the current user and course
                db.execute(
                    "INSERT INTO classes (staff_id, course_id) VALUES (?, ?)",
                    user_id,
                    course_id,
                )

        return redirect("/teachers")

    else:
        profile = db.execute("SELECT * FROM staff WHERE id = ?", user_id)
        department_id = profile[0]["department_id"]

        courses = db.execute(
            "SELECT * FROM courses WHERE id IN (SELECT course_id FROM outlines WHERE program_id = (SELECT id FROM programs WHERE department_id = ?))",
            department_id,
        )

        return render_template("teaching.html", courses=courses, staff=profile)

