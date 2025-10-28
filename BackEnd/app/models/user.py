
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# =====================================================
# USERS TABLE (For authentication)
# =====================================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, faculty, student, etc.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================
# 2. Courses
# ==========================
class Course(db.Model):
    __tablename__ = "courses"
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"))
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True)
    duration = db.Column(db.Integer)  # in semesters or years
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================
# 3. Subjects
# ==========================
class Subject(db.Model):
    __tablename__ = "subjects"
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))  # optional for cross-dept subjects
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True)
    semester = db.Column(db.Integer)
    credits = db.Column(db.Integer)


# ==========================
# 4. Students
# ==========================
class Student(db.Model):
    __tablename__ = "students"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentAcademic(db.Model):
    __tablename__ = "student_academics"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"))
    semester = db.Column(db.Integer)
    marks = db.Column(db.Float)
    grade = db.Column(db.String(5))


# ==========================
# 5. Faculty
# ==========================
class Faculty(db.Model):
    __tablename__ = "faculty"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FacultyAssignment(db.Model):
    __tablename__ = "faculty_assignments"
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="CASCADE"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"))
    semester = db.Column(db.Integer)


# ==========================
# 6. Library
# ==========================
class Book(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20), unique=True)
    copies = db.Column(db.Integer, default=1)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))


class BookIssue(db.Model):
    __tablename__ = "book_issues"
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"))
    issue_date = db.Column(db.Date, default=datetime.utcnow)
    return_date = db.Column(db.Date)
    actual_return_date = db.Column(db.Date)


# ==========================
# 7. Fees
# ==========================
class Fee(db.Model):
    __tablename__ = "fees"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"))
    amount = db.Column(db.Numeric(10,2), nullable=False)
    paid_amount = db.Column(db.Numeric(10,2), default=0)
    due_date = db.Column(db.Date)
    payment_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="Pending")




class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # Seminar, Workshop, Cultural, Sports
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EventParticipant(db.Model):
    __tablename__ = "event_participants"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"))
    participant_type = db.Column(db.String(20), nullable=False)  # 'student' or 'faculty'
    participant_id = db.Column(db.Integer, nullable=False)        # student_id or faculty_id
    role = db.Column(db.String(50))                                # Participant / Organizer / Speaker
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

