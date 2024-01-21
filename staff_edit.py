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
                flash("Old and new passwords are the same. Please enter new a password.")
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
                        "UPDATE staff SET photo_name = ?, photo_hash = ? WHERE id = ?",
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
