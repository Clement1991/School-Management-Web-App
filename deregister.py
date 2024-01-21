from cs50 import SQL
from flask import session, redirect, request
from app import app

db = SQL("sqlite:///school.db")


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
