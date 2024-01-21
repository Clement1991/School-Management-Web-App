import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from validator_collection import validators
from werkzeug.utils import secure_filename
import hashlib
from helpers import login_required


# To provide lists of nationalities or countries.
import pycountry

from app import app

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school.db")

# Create Global variables
GENDER = ["M", "F"]

STATUS = ["Student", "Teaching staff", "Non-teaching staff"]

nationalities = [country.name for country in pycountry.countries]


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    user_id = session["user_id"]
    students = db.execute("SELECT * FROM staff WHERE id = ?", user_id)
    programs = db.execute("SELECT * FROM programs")
    program_id = db.execute("SELECT id FROM programs WHERE name = ?", program)[0][
        "id"
    ]

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

        try:
            email = validators.email(email)
        except:
            flash("Please enter a valid email address!", category="danger")
            return redirect("/edit")

        if len(first_name) < 2 or len(last_name) < 2:
            flash(
                "First name and Last name must have more than 1 character.",
                category="danger",
            )
            return redirect("/edit")
        if not date_of_birth:
            flash("Please enter all fields for date of birth!", category="danger")
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

        # Update staff information if changes have been made
        if first_name != students[0]["first_name"]:
            db.execute(
                "UPDATE students SET first_name = ? WHERE id = ?", first_name, user_id
            )
        if last_name != students[0]["last_name"]:
            db.execute(
                "UPDATE students SET last_name = ? WHERE id = ?", last_name, user_id
            )
        if date_of_birth != students[0]["date_of_birth"]:
            db.execute(
                "UPDATE students SET date_of_birth = ? WHERE id = ?",
                date_of_birth,
                user_id,
            )
        if gender != students[0]["gender"]:
            db.execute("UPDATE students SET gender = ? WHERE id = ?", gender, user_id)
        if nationality != students[0]["nationality"]:
            db.execute(
                "UPDATE students SET nationality = ? WHERE id = ?", nationality, user_id
            )
        if email != students[0]["email"]:
            db.execute("UPDATE students SET email = ? WHERE id = ?", email, user_id)
        if phone != students[0]["phone"]:
            db.execute("UPDATE students SET phone = ? WHERE id = ?", phone, user_id)
        if address != students[0]["address"]:
            db.execute("UPDATE students SET address = ? WHERE id = ?", address, user_id)
        if school != students[0]["previous_school"]:
            db.execute(
                "UPDATE students SET previous_school = ? WHERE id = ?", school, user_id
            )
        if program_id != students[0]["program_id"]:
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
            if not check_password_hash(students[0]["password"], old_password):
                flash("Incorrect old password. Please try again.", category="danger")
                return redirect("/edit")
            
            # Check if new password and confirmation match
            if old_password == new_password:
                flash("Old and new passwords are the same", "danger")
                return redirect("/edit")

            # Check if new password and confirmation match
            if new_password != confirmation:
                flash("New password and confirmation do not match. Please try again.")
                return redirect("/edit")

            # Update the password in the database
            hashed_password = generate_password_hash(new_password)
            db.execute(
                "UPDATE students SET password = ? WHERE id = ?", hashed_password, user_id
            )

            # Forget any user_id
            session.clear()

        # Retrieve the current photo filename and hash from the database
        current_photo = students[0]["photo"]
        current_photo_hash = students[0]["photo_hash"]

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

                    # Update the database with the current photo and photo_hash
                    db.execute(
                        "UPDATE students SET photo = ?, photo_hash = ? WHERE id = ?",
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
        return redirect("/students")

    else:
        return render_template(
            "teachers_edit.html",
            students=students,
            gender=GENDER,
            nationalities=nationalities,
            programs=programs,
        )
