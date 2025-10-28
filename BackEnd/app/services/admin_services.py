
# from app.models.user import (
#     Student, StudentAcademic,
#     Faculty, FacultyAssignment,
#     Department, Course, Subject,
#     Book, BookIssue, Fee,
#     Event, EventParticipant
# )
# from app.db import db
# from datetime import datetime


# from app import db # Assuming 'db' is your SQLAlchemy instance
# from datetime import datetime, date, timedelta
# from app.models.user import User






# # ==============================
# # 1. Student Services
# # ==============================
# def get_all_students():
#     students = Student.query.all()
#     result = []
#     for s in students:
#         result.append({
#             "id": s.id,
#             "name": f"{s.first_name} {s.last_name}",
#             "dob": s.dob,
#             "gender": s.gender,
#             "email": s.email,
#             "phone": s.phone,
#             "address": s.address,
#             "admission_date": s.created_at
#         })
#     return result


# def get_student_detail(student_id):
#     student = Student.query.get_or_404(student_id)
#     academics = StudentAcademic.query.filter_by(student_id=student_id).all()
    
#     subjects_info = []
#     for a in academics:
#         subject = Subject.query.get(a.subject_id)
#         course = Course.query.get(a.course_id)
#         department = Department.query.get(a.department_id)
#         subjects_info.append({
#             "department": department.name if department else None,
#             "course": course.name if course else None,
#             "subject": subject.name if subject else None,
#             "semester": a.semester,
#             "marks": a.marks,
#             "grade": a.grade
#         })
    
#     return {
#         "id": student.id,
#         "name": f"{student.first_name} {student.last_name}",
#         "email": student.email,
#         "phone": student.phone,
#         "address": student.address,
#         "academics": subjects_info
#     }

# def create_student(data):
#     student = Student(
#         first_name=data.get("first_name"),
#         last_name=data.get("last_name"),
#         dob=data.get("dob"),
#         gender=data.get("gender"),
#         email=data.get("email"),
#         phone=data.get("phone"),
#         address=data.get("address"),
#         created_at=datetime.utcnow()
#     )
#     db.session.add(student)
#     db.session.commit()
#     return {"message": "Student created", "id": student.id}

# def update_student(student_id, data):
#     student = Student.query.get_or_404(student_id)
#     student.first_name = data.get("first_name", student.first_name)
#     student.last_name = data.get("last_name", student.last_name)
#     student.dob = data.get("dob", student.dob)
#     student.gender = data.get("gender", student.gender)
#     student.email = data.get("email", student.email)
#     student.phone = data.get("phone", student.phone)
#     student.address = data.get("address", student.address)
#     db.session.commit()
#     return {"message": "Student updated"}

# def delete_student(student_id):
#     student = Student.query.get_or_404(student_id)
#     db.session.delete(student)
#     db.session.commit()
#     return {"message": "Student deleted"}



# app/services/admin_services.py

from app.models.user import (
    Student, StudentAcademic,
    Faculty, FacultyAssignment,
    Department, Course, Subject,
    Book, BookIssue, Fee,
    Event, EventParticipant
)
from app.db import db # PostgreSQL connection
from datetime import datetime, date
from dateutil.parser import parse # Recommended for robust date parsing
from werkzeug.utils import secure_filename
from datetime import datetime
from dateutil.parser import parse
import uuid
import os
import sys

# --- NEW IMPORTS for Non-SQL Databases ---
# NOTE: YOU MUST ENSURE THESE ARE CORRECTLY IMPORTED FROM YOUR INITIALIZATION FILE
from flask import current_app 



# Assuming your MongoDB and Cassandra objects are initialized elsewhere and imported
# Replace 'your_db_init' with the actual module name where you initialized these clients
try:
    from app.services.your_db_init import mongo_collection, session 
except ImportError:
    # Placeholder/Fallback if import path is unknown
    mongo_collection = None 
    session = None 
# ----------------------------------------


# ==============================
# 1. Student Services (Modified for Documents)
# ==============================

def get_all_students():
    # ... (Your existing get_all_students logic) ...
    students = Student.query.all()
    result = []
    for s in students:
        # Convert date/datetime objects to strings for JSON serialization
        dob_str = s.dob.isoformat() if isinstance(s.dob, (date, datetime)) else str(s.dob)
        created_at_str = s.created_at.isoformat() if isinstance(s.created_at, datetime) else str(s.created_at)
        
        result.append({
            "id": s.id,
            "name": f"{s.first_name} {s.last_name}",
            "dob": dob_str,
            "gender": s.gender,
            "email": s.email,
            "phone": s.phone,
            "address": s.address,
            "admission_date": created_at_str
        })
    return result


def get_student_detail(student_id):
    # MODIFIED: Includes fetching document metadata from MongoDB
    student = Student.query.get_or_404(student_id)
    academics = StudentAcademic.query.filter_by(student_id=student_id).all()
    
    subjects_info = []
    for a in academics:
        subject = Subject.query.get(a.subject_id)
        course = Course.query.get(a.course_id)
        department = Department.query.get(a.department_id)
        subjects_info.append({
            "department": department.name if department else None,
            "course": course.name if course else None,
            "subject": subject.name if subject else None,
            "semester": a.semester,
            "marks": float(a.marks), # Ensure it's serializable
            "grade": a.grade
        })
    
    # NEW: Fetch document metadata
    document_metadata = get_student_documents(student_id)
    
    dob_str = student.dob.isoformat() if isinstance(student.dob, (date, datetime)) else str(student.dob)

    return {
        "id": student.id,
        "name": f"{student.first_name} {student.last_name}",
        "email": student.email,
        "phone": student.phone,
        "address": student.address,
        "dob": dob_str,
        "academics": subjects_info,
        "documents": document_metadata # Include document list
    }


def create_student_with_documents(data, files):
    """
    Handles student data insertion into PostgreSQL, file storage in Cassandra, 
    and metadata storage in MongoDB with COMPENSATION logic.
    """
    # CRITICAL FIX: Use 'is None' for PyMongo objects
    if mongo_collection is None or session is None:
        return {"error": "Database connections (Mongo/Cassandra) are not initialized."}, 500

    student_id = None # Initialize to None for error handling

    # 1. PostgreSQL: Create the Student record (Phase 1 Commit)
    try:
        # Robustly parse DOB string to date object
        dob_value = data.get("dob")
        dob_date = parse(dob_value).date() if dob_value else None
        
        student = Student(
            first_name=data.get("first_name"), last_name=data.get("last_name"),
            dob=dob_date, gender=data.get("gender"), email=data.get("email"),
            phone=data.get("phone"), address=data.get("address"), created_at=datetime.utcnow()
        )
        db.session.add(student)
        db.session.commit() # Commit PENDING: We need the student_id
        student_id = student.id
        
    except Exception as e:
        db.session.rollback()
        print(f"PostgreSQL Student creation failed: {str(e)}", file=sys.stderr)
        return {"error": f"PostgreSQL Student creation failed: {str(e)}"}, 500

    # 2. Cassandra/MongoDB: Handle Documents (Phase 2 Commit/Compensating Action)
    uploaded_docs = []
    upload_folder = current_app.config['UPLOAD_FOLDER'] 
    
    # Track success of Phase 2
    document_upload_successful = True

    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(upload_folder, filename)
            
            try:
                file.save(temp_path)
                with open(temp_path, 'rb') as f:
                    file_data = f.read()

                doc_id = uuid.uuid4()
                upload_time = datetime.utcnow()
                
                # Insert into Cassandra (Binary Data)
                session.execute(
                    """
                    INSERT INTO student_files (doc_id, student_id, file_name, file_data, upload_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (doc_id, student_id, filename, file_data, upload_time)
                )

                # Insert metadata into MongoDB (Link: student_id -> doc_id)
                metadata = {
                    "student_id": student_id, "document_id": str(doc_id),
                    "file_name": filename, "file_type": filename.split('.')[-1],
                    "upload_date": upload_time, "version": 1 
                }
                mongo_collection.insert_one(metadata)
                
                uploaded_docs.append({"document_id": str(doc_id), "file_name": filename})

            except Exception as e:
                # CRITICAL FAILURE: Document upload failed for one or more files
                print(f"CRITICAL Document storage failure for student {student_id}: {str(e)}", file=sys.stderr)
                document_upload_successful = False
                # Stop processing files, as we're going to rollback the Postgres record anyway
                break 
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # 3. Final Check and Compensation
    if not document_upload_successful:
        # COMPENSATING ACTION: Delete the PostgreSQL record
        # Note: You would also need a cleanup function here for Cassandra/Mongo if partial docs were saved
        
        # Get the student object back to delete it
        student_to_delete = Student.query.get(student_id)
        if student_to_delete:
            db.session.delete(student_to_delete)
            db.session.commit() # Rollback the PostgreSQL change
        
        return {
            "error": "Document storage failed. Student record rolled back.", 
            "detail": f"PostgreSQL student record with ID {student_id} was deleted to maintain consistency."
        }, 500


    return {
        "message": "Student created successfully.", 
        "id": student_id,
        "documents_uploaded": uploaded_docs
    }, 201
# Rename the original function to avoid confusion if needed, 
# but the route now calls the new one.
# def create_student(data): # This function is now superseded by create_student_with_documents
#     ...

def update_student(student_id, data):
    # ... (Your existing update_student logic) ...
    student = Student.query.get_or_404(student_id)
    student.first_name = data.get("first_name", student.first_name)
    # Handle date conversion for DOB update
    dob_value = data.get("dob")
    if dob_value:
        try:
            student.dob = parse(dob_value).date()
        except Exception:
            pass # Ignore if format is bad
            
    student.last_name = data.get("last_name", student.last_name)
    student.gender = data.get("gender", student.gender)
    student.email = data.get("email", student.email)
    student.phone = data.get("phone", student.phone)
    student.address = data.get("address", student.address)
    db.session.commit()
    return {"message": "Student updated"}

def delete_student(student_id):
    # ... (Your existing delete_student logic) ...
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return {"message": "Student deleted"}


# =====================================================
# NEW STUDENT DOCUMENT Functions (called by get_student_detail)
# =====================================================

def get_student_documents(student_id):
    """Fetches document metadata from MongoDB for a given student_id."""
    if not mongo_collection:
        return []
        
    documents_cursor = mongo_collection.find({"student_id": student_id})
    
    result = []
    for doc in documents_cursor:
        # Convert datetime objects to ISO strings for JSON
        upload_date_str = doc.get("upload_date").isoformat() if doc.get("upload_date") else None
        
        result.append({
            "document_id": doc.get("document_id"),
            "file_name": doc.get("file_name"),
            "file_type": doc.get("file_type"),
            "upload_date": upload_date_str,
            "version": doc.get("version")
        })
    return result


def download_student_document(doc_id):
    """
    Retrieves the file data and name from Cassandra using the document_id.
    
    Returns: (file_data_bytes, file_name_str) or (None, None)
    """
    if not session:
        return None, None
        
    try:
        doc_uuid = uuid.UUID(doc_id)
    except ValueError:
        return None, None
        
    row = session.execute(
        "SELECT file_name, file_data FROM student_files WHERE doc_id=%s",
        (doc_uuid,)
    ).one_or_none()

    if row:
        return row.file_data, row.file_name
    else:
        return None, None

# ... (Rest of Faculty, Library, Fees, Events services remain the same) ...

# ==============================
# 2. Faculty Services
# ==============================
def get_all_faculty():
    faculties = Faculty.query.all()
    result = []
    for f in faculties:
        result.append({
            "id": f.id,
            "name": f"{f.first_name} {f.last_name}",
            "email": f.email,
            "phone": f.phone,
            "address": f.address,
            "joining_date": f.created_at
        })
    return result

def get_faculty_detail(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    assignments = FacultyAssignment.query.filter_by(faculty_id=faculty_id).all()
    
    subjects_info = []
    for a in assignments:
        subject = Subject.query.get(a.subject_id)
        course = Course.query.get(a.course_id)
        department = Department.query.get(a.department_id)
        subjects_info.append({
            "department": department.name if department else None,
            "course": course.name if course else None,
            "subject": subject.name if subject else None,
            "semester": a.semester
        })
    
    return {
        "id": faculty.id,
        "name": f"{faculty.first_name} {faculty.last_name}",
        "email": faculty.email,
        "phone": faculty.phone,
        "address": faculty.address,
        "assignments": subjects_info
    }

def create_faculty(data):
    faculty = Faculty(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address"),
        created_at=datetime.utcnow()
    )
    db.session.add(faculty)
    db.session.commit()
    return {"message": "Faculty created", "id": faculty.id}

def update_faculty(faculty_id, data):
    faculty = Faculty.query.get_or_404(faculty_id)
    faculty.first_name = data.get("first_name", faculty.first_name)
    faculty.last_name = data.get("last_name", faculty.last_name)
    faculty.email = data.get("email", faculty.email)
    faculty.phone = data.get("phone", faculty.phone)
    faculty.address = data.get("address", faculty.address)
    db.session.commit()
    return {"message": "Faculty updated"}

def delete_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    db.session.delete(faculty)
    db.session.commit()
    return {"message": "Faculty deleted"}


# ==============================
# 3. Library Services
# ==============================
def get_all_books():
    books = Book.query.all()
    result = []
    for b in books:
        result.append({
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "copies": b.copies,
        })
    return result

def get_all_book_issues():
    issues = BookIssue.query.all()
    result = []
    for i in issues:
        student = Student.query.get(i.student_id)
        book = Book.query.get(i.book_id)
        result.append({
            "student": f"{student.first_name} {student.last_name}" if student else None,
            "book": book.title if book else None,
            "issue_date": i.issue_date,
            "return_date": i.return_date,
            "actual_return_date": i.actual_return_date
        })
    return result

def add_book(data):
    book = Book(
        title=data.get("title"),
        author=data.get("author"),
        isbn=data.get("isbn"),
        copies=data.get("copies", 1)
    )
    db.session.add(book)
    db.session.commit()
    return {"message": "Book added", "id": book.id}

def issue_book(data):
    issue = BookIssue(
        student_id=data.get("student_id"),
        book_id=data.get("book_id"),
        issue_date=datetime.utcnow(),
        return_date=data.get("return_date")
    )
    db.session.add(issue)
    db.session.commit()
    return {"message": "Book issued", "id": issue.id}

def return_book(issue_id, data):
    issue = BookIssue.query.get_or_404(issue_id)
    issue.actual_return_date = data.get("actual_return_date", datetime.utcnow())
    db.session.commit()
    return {"message": "Book returned"}


# ==============================
# 4. Fees
# ==============================
def get_all_fees():
    fees = Fee.query.all()
    result = []
    for f in fees:
        student = Student.query.get(f.student_id)
        result.append({
            "student": f"{student.first_name} {student.last_name}" if student else None,
            "amount": float(f.amount),
            "paid_amount": float(f.paid_amount),
            "due_date": f.due_date,
            "payment_date": f.payment_date,
            "status": f.status
        })
    return result


# ==============================
# 5. Events
# ==============================
def get_all_events():
    events = Event.query.all()
    result = []
    for e in events:
        result.append({
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "event_type": e.event_type,
            "date": e.date,
            "location": e.location
        })
    return result

def get_event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    participants = EventParticipant.query.filter_by(event_id=event_id).all()
    
    participant_list = []
    for p in participants:
        name = None
        if p.participant_type == "student":
            student = Student.query.get(p.participant_id)
            if student:
                name = f"{student.first_name} {student.last_name}"
        elif p.participant_type == "faculty":
            faculty = Faculty.query.get(p.participant_id)
            if faculty:
                name = f"{faculty.first_name} {faculty.last_name}"
        
        participant_list.append({
            "id": p.id,
            "type": p.participant_type,
            "name": name,
            "role": p.role,
            "registered_at": p.registered_at
        })
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "date": event.date,
        "location": event.location,
        "participants": participant_list
    }

def create_event(data):
    event = Event(
        title=data.get("title"),
        description=data.get("description"),
        event_type=data.get("event_type"),
        date=data.get("date"),
        location=data.get("location")
    )
    db.session.add(event)
    db.session.commit()
    return {"message": "Event created", "id": event.id}

def update_event(event_id, data):
    event = Event.query.get_or_404(event_id)
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.event_type = data.get("event_type", event.event_type)
    event.date = data.get("date", event.date)
    event.location = data.get("location", event.location)
    db.session.commit()
    return {"message": "Event updated"}

def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}
