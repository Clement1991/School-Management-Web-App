# SCHOOL MANAGEMENT WEB APPLICATION

By Clement Gyasi Siaw

Video overview: <https://www.youtube.com/watch?v=SAJjHrtwWbQ>

## Scope

This project is a School Management Web Application of an engineering faculty in a University. The faculty has three departments with seven programs offered to propective students. This app was built with `Flask`. It is a user-friendly platform that caters for students, teaching staff and non-teaching staff, providing features for each user category.

### Key Features:

* `User-Specific Dashboards`: Students can view the names of all departments and programs and receive important announcements. Teaching staff have access to profile details, courses they teach, and upcoming events. Non-teaching staff can manage their profiles and department-specific information.
* `Profile Management`: Users can easily update and manage their personal information, including photos, contact details and other relevant information.
* `Courses and Programs`: Students can explore available courses and programs and view their course schedule. Teaching staff can manage the courses they teach, add new courses and remove old ones. Non-teaching staff can access relevant department information.
* `Announcements and Events`: Stay informed about upcoming events, examinations, and important announcements directly through the platform.
* `Registration and Authentication`: Seamless registration process with multi-level authentication for enhanced security.
* `Responsive Design`: The school web application is designed with a responsive layout, ensuring accessibility across various devices.
* `Database Management`: The database includes all entities neccessary to facilitate the running of the web application: As such, included in the database are entities like students, staff, departments, programs, courses, classes and outlines.
* `User logs`: User acativities the web application are kept on log tables in the database for record keeping.

Out of scope of this web application are elements like certificates, transcripts, class schedules and leacture room numbers, course attendance records of students, exam schedules, student and teacher timetables, library inventory, health, disciplinary and behavioral records of students and other attributes.

## Understanding

### app.py

Atop the `app.py` file are a bunch of imports, among them is Havard's CS50’s SQL module and a few helper functions. Also included are imports of other route blueprints from separate files. The routes have been separated from the main `app.py` file in other to enhance readability and understanding.
After configuring Flask, this file disables caching of responses, else the browser will not notice any changes made to the file. It then further configures Flask to store sessions on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask’s default. It is also configured to only allow the upload of photos with certain types of extensions. The file then configures CS50’s SQL module to use school.db which is a SQlite database.
Global variables `STATUS` and `GENDER` are also defined. STATUS determines the type of user; whether student, teaching staff or non-teaching staff is using the app. GENDER also defines `M` and `F` for male and female users respectively. After that, there are a number of routes which will be discussed later in detail.

### helpers.py

This file contains the `login_required` function. The function is used to automatically direct users to the login route if the user has not logged in or after a user logs out of the app.

### requirements.txt

That file simply prescribes the packages on which this app will depend.

### static/

Inside the static folder is `styles.css`, `app.js` and the `photos` folder. The style.css file contains some css where as app.js contains javascript code which will be discussed in detail later. The photos folder is created to store all photos uploaded by users with very unique filenames.

### Templates/

The templates folder contains templates used to build the web app, stylized with Bootstrap. `layout.html` is the base template to which all other templates are linked. It has a sidebar which displays different routes based on the status of the user who has logged in. If no user has logged in, it only displays "Welcome to MySchool App". `layout.html` also defines a block, `main`, inside of which all templates shall go. It also includes support for Flask’s message flashing so that messages can be relayed from one route to another for the user to see. The other templates will be discussed in great detail later in this report.

### schema.sql

This files contains the schema, indexes, log tables and all other entities in the database.

### queries.sql

This file contains initial `INSERT` statements that insert relevant information into tables such as departments, programs, courses and outlines.

### school.db

This is the databse which contains all the relevant tables which will be used to manage all data of the school web application. Some tables have already been pre-filled as we discussed earlier while others will be filled based on user status and type of information the user provides.

## Specification

### register.py and register.html

The `register.py` file contains the `/register` route which is used to register users into the database. This route is linked to the `register.html` template which generates the registration form for users to fill and submit.
Atop `register.py` contains various imports including `generate_password_hash` from `werkzeug.security` for generating hashed passwords of users. It also configures Flask app to specify the photo upload folder which is the photos folder located inside the static folder. Other imports are `validators` which is used to validate email addresses for authenticity. `pycountry` is also imported to generate a list of all countries in the world.
The registration template is generated by `register.html`. With the exception of the photograph field, user is required to complete all fields. If a user selects `Student` as status, the `department` field disappears, otherwise, the `program` and `school` fields disappear for a non-student status.
If photo is uploaded, it is also validated for required extensions. `hashlib` import is used to generate a hash content called `photo_hash` of the photo and this in addition to the user's first and last names is used to generate a unique filename called `photo_name` for the user and stored in the photos folder which is located in the static folder. Users would also have to confirm their passwords after which the passwords are hashed using `generate_password_hash`.
All required fields are then validated and authenticated using flash messages when necessary. If a user selects a `Student` status, a query is sent to the `students` table in the database to verify if the email provided by the user already exists. If true, a flash message is sent to deny the registration and user is asked to input a different email address. If the email is not found in the database, all the relevant information provided is inserted into the `students` table to create a record for the student. For `Teaching` and `Non-teaching` staff statuses, the same procedure is repeated but this time, on the `staff` table in the database.
After succesful registration, the user is directed to the homepage which subsequently redirects the user to the login page using the `login_required` function.

### login.py and login.html

The `login.py` file contains the `/login` route which is linked to `login.html` to provide a template for users to login. All fields are first validated. After that, if a user has selected `Student` as status, the database is queried to select any record from the `students` table with the same email as provided by the user in the login page. If no record is found, the user is prompted to provided a new email address. If a record is found, `check_password_hash` is used to compare the hashed password in the found record and that provided by the user in the login page. If they are the same, the user is successfully logged in and directed to the root directory `/dashboard` which together with other routes, form part of the the students page. If the hash passwords are different, the user is prompted to provide a correct password.
The same procedure is followed if a user selects `Teaching staff` or `Non-teaching staff` as status but the `staff` table in the database is rather queried instead of the students table. When a user logs in, different pages containing different routes are displayed depending on the user's status. The `/dashboard` route is present in all pages. The user's `id` from the found record and the status selected from the login page is stored in Flask's `session` for identification.
When the `Login` button is clicked, the users information is sent to either the `student_logs` or `staff_logs` table in the database depending on the status of the user. The login time is also recorded on these log tables.

### /dashboard and dashboard.html

`/dashboard` is the root route of the web app connected to the `dashboard.html` template. It contains quicks link such as `/programs` (programs.html), `/departments` (departments.html), announcements etc. These routes are located in `app.py`. Every user has access to the `/dashboard` route.

### /students and students.html

The `/students` route, found in `app.py` is linked to the `students.html` template to display the profile of the logged in student. The user id stored in session during login, is used to seleect all information of the student from the `students` table in the database. The program id from the student record is used to select the name of the department which teaches the program from the `departments` table. All relevant information related to the student is displayed in the student's profile by the `students.html` template. This template also provides a link to edit and delete the student's profile.

### students_edit.py and edit.html

The `students.html` template provides the link to `edit.html`, which is the template for editing students' profile. `students_edit.py` contains the `/edit` route responsible updating students' records. The `edit.html` template is designed to be prefilled with the logged in student's information. The student's id stored in session during login is used to select their data from the database. After submitting `edit.html` via POST, a validation process of student's information is carried out just like in register.py. If all values from the template pass this validation, the values are then compared to their corresponding column values in the students table. If any value is different from their values in the students table, the database value is updated to the new value provided in edit.html. Otherwise, no values are updated if all values are the same. After a succesful update, the route is redirected back to the student's profile at `students.html` and any updates are automatically visible on the profile.

### deregister.py

The `students.html` template contains a `Delete Profile` button. When that button is clicked, a form is sent to the `/deregister` route which is found in the `deregister.py` file. It's function is to use the student's id to delete any record from the `students` table in the database with the same `id`, thereby deleting the student's profile. The `/deregister` route is also found in `teachers.html` and `staff.html` and does the same job by deleting teachers and non-teaching staff profiles. After deleting the profile, the session is cleared and the user is redirected to the login page.


### /courses and courses.html

`app.py` contains the `/courses` route which is linked to the `courses.html` template which is responsible for displaying all the courses which are registered to the student's chosen program. The year that each course would be taken is also displayed.

### /teachers and teachers.html, /teaching

`/teachers` and `teachers.html` work in the same way as `/students` and `students.html` as described above. In this case, all teachers' profile queries are done on the `staff` table in the database. There is also an `Add Courses` button which directs the teacher to the `/courses` route located in `app.py`. This route is linked to the `courses.html` template to provide teachers with the names of all courses that are taught in their department for them to select a list of courses that they teach.
When courses are selected and the `Save` button is clicked, the `id`'s of each selected course is sent to the `/teaching` route which is linked to the `teaching.html` template. This route inserts the teacher's id and the ids of each selected course into the `classes` table row by row. This indicates that, the teacher teaches that course. If any course has already been selected by the teacher, that course is ignored and not inserted into the classes table, since there would be a course_id-teacher_id combination already existing on the classes table and adding the same combination would raise a PRIMARY KEY constraint.
The classes table is automatically queried inside the `/teachers` route to display the names of all courses taught by the teacher in the teacher's profile. Beside every added course is the `Remove Course` button. When clicked on, the course `id` is sent to the `/remove` route located in `app.py`. This route uses the course id together with the teachers id to delete any row on the `classes` table that contains both ids. This deletion from the classes table indicates that, the teacher no longer teaches that course and is therefore automatically updated on the teachers profile with the name of that particular absent.

### teachers_edit.py and teachers_edit.html

`teachers.html` template provides a link for teachers to edit their profiles just as we discussed above with students' profiles. `teachers_edit.py` and `teachers_edit.html` are used to carry out the same editing and updating activities just as `students_edit.py` and `edit.html` above. In this case, all staff profile queries are done on the `staff` table in the database instead of the `students` table. After saving, the user is redirected to the teacher's profile in `teachers.html`.

### /staff and staff.html

`/staff` and `staff_edit.py` work in the same way as `/students` and `students.html` as described above. In this case, all profile queries are done on `staff` table in the database.

### staff_edit.py and staff_edit.html

These two files work the same way as other profile editors described above to edit the profiles of `Non-teaching staff` on the web application. All records of non-teaching staff are stored on the `staff` table in the database for queries.

### /logout

When the `Logout` button is clicked, the users information is sent to either the `student_logs` or `staff_logs` table in the database depending on the status of the user. The logouts time is also recorded on these log tables.

## Optimizations

Per the typical searches on the web app, users may want to have a quick view of all the names of the departments and programs offered by the engineering faculty in the dashboard. As a result, indexes have been created on the `name` columns of the `departments` and `programs` tables in the database to speed up search. 

## Limitations

The current web application does not provide information on students' fee payment records.
