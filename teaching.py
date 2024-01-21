from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
from app import app

db = SQL("sqlite:///school.db")


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
