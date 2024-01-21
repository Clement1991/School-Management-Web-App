-- Drop tables
DROP TABLE IF EXISTS "classes";
DROP TABLE IF EXISTS "outlines";
DROP TABLE IF EXISTS "students";
DROP TABLE IF EXISTS "student_logs";
DROP TABLE IF EXISTS "programs";
DROP TABLE IF EXISTS "courses";
DROP TABLE IF EXISTS "staff";
DROP TABLE IF EXISTS "staff_logs";
DROP TABLE IF EXISTS "departments";

-- Drop triggers
DROP TRIGGER IF EXISTS "log_student_updates";
DROP TRIGGER IF EXISTS "log_student_deletes";
DROP TRIGGER IF EXISTS "log_student_inserts";
DROP TRIGGER IF EXISTS "log_staff_updates";
DROP TRIGGER IF EXISTS "log_staff_deletes";
DROP TRIGGER IF EXISTS "log_staff_inserts";

---- Drop indexes
DROP INDEX IF EXISTS "program_index";
DROP INDEX IF EXISTS "department_index";

-- Clean up unused space
VACUUM;


CREATE TABLE "students" (
    "id" INTEGER,
    "photo" TEXT,
    "photo_hash" TEXT,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "date_of_birth" NUMERIC NOT NULL,
    "gender" TEXT NOT NULL CHECK("gender" IN('M', 'F')),
    "nationality" TEXT NOT NULL,
    "previous_school" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT UNIQUE NOT NULL,
    "phone" TEXT NOT NULL,
    "address" TEXT NOT NULL,
    "program_id" INTEGER,
    "started" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("program_id") REFERENCES "programs"("id")
);


CREATE TABLE "staff" (
    "id" INTEGER,
    "photo" TEXT,
    "photo_hash" TEXT,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "date_of_birth" NUMERIC NOT NULL,
    "gender" TEXT NOT NULL CHECK("gender" IN('M', 'F')),
    "nationality" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT UNIQUE NOT NULL,
    "phone" TEXT NOT NULL,
    "address" TEXT NOT NULL,
    "department_id" INTEGER,
    "status" TEXT NOT NULL CHECK("status" IN('Teaching staff', 'Non-teaching staff')),
    "started" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("department_id") REFERENCES "departments"("id")
);


CREATE TABLE "student_logs" (
    "id" INTEGER,
    "type" TEXT NOT NULL,
    "old_email" TEXT,
    "new_email" TEXT,
    "old_password" TEXT,
    "new_password" TEXT,
    "timestamp" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id")
);


CREATE TABLE "staff_logs" (
    "id" INTEGER,
    "type" TEXT NOT NULL,
    "old_email" TEXT,
    "new_email" TEXT,
    "old_password" TEXT,
    "new_password" TEXT,
    "timestamp" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id")
);


CREATE TABLE "departments" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);


CREATE TABLE "programs" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "degree" INTEGER NOT NULL,
    "department_id" INTEGER,
    "duration_years" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("department_id") REFERENCES "departments"("id")
);


CREATE TABLE "courses" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);


CREATE TABLE "outlines" (
    "program_id" INTEGER,
    "course_id" INTEGER,
    "year" INTEGER NOT NULL,
    PRIMARY KEY("program_id", "course_id"),
    FOREIGN KEY("course_id") REFERENCES "courses"("id"),
    FOREIGN KEY("program_id") REFERENCES "programs"("id")
);


CREATE TABLE "classes" (
    "staff_id" INTEGER,
    "course_id" INTEGER,
    PRIMARY KEY("staff_id", "course_id"),
    FOREIGN KEY("staff_id") REFERENCES "staff"("id") ON DELETE CASCADE,
    FOREIGN KEY("course_id") REFERENCES "courses"("id")
);

-- User logs
CREATE TRIGGER "log_student_updates"
AFTER UPDATE OF "email", "password" ON "students"
FOR EACH ROW
BEGIN
    INSERT INTO "student_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('update', OLD."email", NEW."email", OLD."password", NEW."password");
END;

CREATE TRIGGER "log_student_deletes"
AFTER DELETE ON "students"
FOR EACH ROW
BEGIN
    INSERT INTO "student_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('delete', OLD."email", NULL, OLD."password", NULL);
END;

CREATE TRIGGER "log_student_inserts"
AFTER INSERT ON "students"
FOR EACH ROW
BEGIN
    INSERT INTO "student_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('insert', NULL, NEW."email", NULL, NEW."password");
END;

CREATE TRIGGER "log_staff_updates"
AFTER UPDATE OF "email", "password" ON "staff"
FOR EACH ROW
BEGIN
    INSERT INTO "staff_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('update', OLD."email", NEW."email", OLD."password", NEW."password");
END;

CREATE TRIGGER "log_staff_deletes"
AFTER DELETE ON "staff"
FOR EACH ROW
BEGIN
    INSERT INTO "staff_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('delete', OLD."email", NULL, OLD."password", NULL);
END;

CREATE TRIGGER "log_staff_inserts"
AFTER INSERT ON "staff"
FOR EACH ROW
BEGIN
    INSERT INTO "staff_logs" ("type", "old_email", "new_email", "old_password", "new_password")
    VALUES ('insert', NULL, NEW."email", NULL, NEW."password");
END;

-- Indexes to speed common searches
CREATE INDEX "program_index" ON "programs" ("name");
CREATE INDEX "department_index" ON "departments" ("name");
