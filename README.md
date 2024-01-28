# SCHOOL MANAGEMENT WEB APPLICATION

By Clement Gyasi Siaw

Video overview: [Watch Video Overview](https://www.youtube.com/watch?v=SAJjHrtwWbQ)  
Web app: [School Management Web Application](https://my-school-web-app-f0284fad144a.herokuapp.com)


## Scope

This project is a School Management Web Application of an engineering faculty in a University. The faculty has three departments with seven programs offered to propective students. This app is built with `Flask`. It is a user-friendly platform that caters for students, teaching staff and non-teaching staff, providing features for each user category.

### Key Features:

* `User-Specific Dashboards`: Students can view the names of all departments and programs and receive important announcements. Teaching staff have access to profile details, courses they teach, and upcoming events. Non-teaching staff can manage their profiles and department-specific information.
* `Profile Management`: Users can easily update and manage their personal information, including photos, contact details and other relevant information.
* `Courses and Programs`: Students can explore available courses and programs and view their course schedule. Teaching staff can manage the courses they teach, add new courses and remove old ones. Non-teaching staff can access relevant department information.
* `Announcements and Events`: Stay informed about upcoming events, examinations, and important announcements directly through the platform.
* `Registration and Authentication`: Seamless registration process with multi-level authentication for enhanced security.
* `Responsive Design`: The school web application is designed with a responsive layout, ensuring accessibility across various devices.
* `Database Management`: The database includes all entities neccessary to facilitate the running of the web application: As such, included in the database are entities like students, staff, departments, programs, courses, classes and outlines.
* `User logs`: User activities on the web application are kept on log tables in the database for record keeping.

Out of scope of this web application are elements like certificates, transcripts, class schedules and leacture room numbers, course attendance records of students, exam schedules, student and teacher timetables, library inventory, health, disciplinary and behavioral records of students and other attributes.

## Running

In vs-code navigate to the root directory and create a virtual environment (venv) and activate the venv depending on the operating system. In the same root directory run `sqlite3 school.db` to open school.db with sqlite3. When you run `.schema ` in the SQLite prompt, school.db comes with several entities. After running `flask run` in the terminal, open the link given in a browser to access the web application.

## Understanding

### app.py

Atop `app.py` are a bunch of imports, among them is Havard's CS50’s SQL module and a few helper functions. Other imports include `generate_password_hash` from `werkzeug.security` used for generating hashed passwords of users. There is also `validators` which is used to validate email addresses for authenticity. `pycountry` is imported to generate a list of all countries in the world.
After configuring Flask, this file disables caching of responses, else the browser will not notice any changes made to the file. It also configures Flask app to specify the photo upload folder which is located inside the `/static` folder. Flask then stores sessions on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask’s default. It is also configured to only allow the upload of photos with certain types of extensions. This file then configures CS50’s SQL module to use school.db which is a SQlite database.
Global variables `STATUS` and `GENDER` are also defined. STATUS determines the type of user; whether a `Student`, `Teaching staff` or `Non-teaching staff` is using the app. GENDER also defines `M` and `F` for male and female users respectively. After that, there are a number of routes which will be discussed later in detail.

### helpers.py

This file contains the `login_required` function. The function is used to automatically direct users to the login route if the user has not logged in or after a user logs out of the app.

### requirements.txt

That file simply prescribes the packages on which this app depends.

### static/

Inside the static folder is `styles.css`, `app.js` and the `photos` folder. The style.css file contains some css where as app.js contains javascript code which will be discussed in detail later. The photos folder is created to store all photos uploaded by users with very unique filenames.

### Templates/

The templates folder contains templates used to build the web app, stylized with Bootstrap. `layout.html` is the base template to which all other templates are linked. It has a sidebar which displays different routes based on the status of the user who has logged in. If no user has logged in, it only displays "Welcome to MySchool App". `layout.html` also defines a block, `main`, inside of which all templates shall go. It also includes support for Flask’s message flashing so that messages can be relayed from one route to another for the user to see. The other templates will be discussed in great detail later in this report.

### schema.sql

This files contains the schema, indexes, log tables and all other entities of the database. You can reset the database by running `.read schema.sql` in sqlite3.

### queries.sql

This file contains initial `INSERT` statements that insert relevant information into tables such as departments, programs, courses and outlines.

### school.db

This is the databse which contains all the relevant tables that will be used to manage all data of the web application. Some tables have already been pre-filled as we discussed earlier while others will be filled based on user status and type of information the user provides.

## Specification

### /register and register.html

The `/register` route in `app.py` allows a user to register for an account via `register.html`. With the exception of the photograph field, a user is required complete all fields. If a user selects `Student` as status, the `department` field disappears. Users with `Teaching staff` and `Non-teaching staff` statuses are not required to fill the `program` and `school` fields. This is made possible by a function displayed in `app.js`
If a photo is uploaded, it is validated for required extensions. `hashlib` is used to generate a `photo_hash` content which is then used to generate a unique `photo_name` for the user's photo. Users are required to confirm their passwords after which the passwords are hashed using `generate_password_hash`. If a required field is filled with wrong input or is left blank, a flash message is used to prompt the user for correction. Before a user submits the registration form, there is a check to ensure that, the email provided does not already exist in the database.
After a successful registration, all students' information are inserted into the `students` table while staff information goes to the `staff` table in the database. Registration date and time is also recorded on log tables in the database. The user is directed to the homepage which subsequently redirects the user to the login page using the `login_required` function.

### /login and login.html

The `/login` route in `app.py` is used to log users into their account via `login.html`. Validation is done to ensure that, the email and password provided by the user exists in the database. If user account exists, the user is successfully logged in and directed to the root directory `/dashboard`. Otherwise, the user is prompted to provide correct information. After login, users are presented with different sets of routes based on their status.
The user's `id` from the database and their status are stored in Flask's `session` for identification. Login time, email and password are also stored on the `student_logs` or `staff_logs` table in the database depending on the status of the user.

### /dashboard and dashboard.html

`/dashboard` is the root route of the web app connected to the `dashboard.html` template. It contains quicks link such as `/programs` (programs.html), `/departments` (departments.html), announcements etc. These routes are located in `app.py`. Every user has access to the `/dashboard` route.

### /students and students.html

The `/students` route via `students.html` displays the profile of the logged in student. The `user_id` stored in `session` during login, is used to seleect all information of the student from the `students` table in the database. The `program_id` from the student's record is used to select the name of the department which teaches the program the student is enrolled in from the `departments` table. All relevant information related to the student is displayed in the student's profile. This template also provides a link to `edit` and `delete` the student's profile.

### /students_edit and edit.html

The `/edit` route via `edit.html` is used to edit and update students' records. The `edit.html` template is designed to be prefilled with the logged in student's information. After editing, a validation process of student's information is carried out in the same way as in `/register` above. If validation is successful, the values are then compared to their corresponding column values in the students table. If any two corresponding values are different, the database value is updated to the new value provided in edit.html. Otherwise, there are no updates. After a succesful update, the route is redirected back to the student's profile at `students.html` and any updates become automatically visible on the profile. If there is an email or password update, the old and new values are recorded on the `student_logs` table in the database.


### /courses and courses.html

`/courses` via `courses.html` displays all the courses which are registered to the student's chosen program. The year that each course would be taken is also displayed.

### /teachers and teachers.html, /teaching

`/teachers` and `teachers.html` work in the same way as `/students` and `students.html` as described above. But in this case, all teachers' profile queries are done on the `staff` table in the database. There is also an `Add Courses` button connected to `/courses` which displays the names of all courses that are taught in the teacher's department via `courses.html`, in order for the teacher to select a list of courses that he / she teaches.
When courses are selected and the `Save` button is clicked, the `id`'s of each selected course is sent to the `/teaching` route which is linked to `teaching.html`. This route inserts the teacher's id (user_id) and the ids of each of the selected courses into the `classes` table row by row. If any selected course has already been selected by the teacher, that course is ignored and not inserted into the classes table, since this would raise a PRIMARY KEY constraint.
The `classes` table is then automatically queried inside the `/teachers` route to display the names of all courses taught by the teacher in the teacher's profile. Beside every selected course is the `Remove Course` button. When clicked on, the course `id` is sent to the `/remove` route. This route uses the course id together with the teachers id to delete any row on the `classes` table that contains the combination of both ids. This deletion from the classes table indicates that, the teacher no longer teaches that course and is therefore automatically deleted from the taught courses on the teachers profile. 


### /teachers_edit and teachers_edit.html

`teachers.html` template provides a link to `/teachers_edit` and `teachers_edit.html` for teachers to edit and update their profiles just as we discussed above with editing students' profiles. After saving, the user is redirected to the teacher's profile in `teachers.html`.

### /staff and staff.html

`/staff` and `staff.html` work in a similar way as `/teachers` and `teachers.html` as described above. Because they have a `Non-teaching staff` status, they cannot select any courses to teach. However they can view relevant department information from the dahboard.

### /staff_edit and staff_edit.html

They work in a similar way as `/teachers_edit` and `teachers_edit.html` above to edit the profiles of `Non-teaching staff` on the web application. All records of non-teaching staff are stored on the `staff` table in the database for queries.

### /deregister

The `students.html` template contains a `Delete Profile` button which is connected to `/deregister`. It's function is to use the logged in `user_id` to delete any record from the `students` or `staff` table in the database with the same `id`, thereby deleting the user's profile. After deleting the profile, the session is cleared and the user is redirected to the login page.

### /logout

When the `Logout` button is clicked, the users information is sent to either the `student_logs` or `staff_logs` table in the database depending on the status of the user. The logouts time is also recorded on these log tables.

## Optimizations

Per the typical searches on the web app, users may want to have a quick view of all the names of the departments and programs offered by the engineering faculty in the dashboard. As a result, indexes have been created on the `name` columns of the `departments` and `programs` tables in the database to speed up search. 

## Limitations

The current web application does not provide information on students' fee payment records.
