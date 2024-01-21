from cs50 import SQL
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school.db")

# Create Global variables
GENDER = ["M", "F"]

STATUS = ["Student", "Teaching staff", "Non-teaching staff"]


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
