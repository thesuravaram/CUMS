
from app.models.user import (
    Student, StudentAcademic,
    Faculty, FacultyAssignment,
    Department, Course, Subject,
    Book, BookIssue, Fee,
    Event, EventParticipant
)
from app.db import db
from datetime import datetime


from app import db # Assuming 'db' is your SQLAlchemy instance
from datetime import datetime, date, timedelta
from app.models.user import User

def add_sample_users():
    """Adds 5 sample User records (1 admin, 2 faculty, 2 students)."""
    print("Adding sample Users...")
    users_data = [
        {'email': 'admin@college.edu', 'role': 'admin', 'password': 'AdminPassword1'},
        {'email': 'prof.smith@college.edu', 'role': 'faculty', 'password': 'FacultyPassword1'},
        {'email': 'dr.jones@college.edu', 'role': 'faculty', 'password': 'FacultyPassword2'},
        {'email': 'student1@college.edu', 'role': 'student', 'password': 'StudentPassword1'},
        {'email': 'student2@college.edu', 'role': 'student', 'password': 'StudentPassword2'}
    ]
    for data in users_data:
        user = User(email=data['email'], role=data['role'])
        user.set_password(data['password'])
        db.session.add(user)
    db.session.commit()
    print(f"Added {len(users_data)} Users.")

def add_sample_departments():
    """Adds 5 sample Department records."""
    print("Adding sample Departments...")
    departments_data = [
        {'name': 'Computer Science', 'code': 'CS', 'created_at': datetime(2000, 1, 1)},
        {'name': 'Electrical Engineering', 'code': 'EE', 'created_at': datetime(2002, 5, 15)},
        {'name': 'Mechanical Engineering', 'code': 'ME', 'created_at': datetime(1998, 9, 10)},
        {'name': 'Physics', 'code': 'PHY', 'created_at': datetime(2005, 3, 20)},
        {'name': 'Mathematics', 'code': 'MATH', 'created_at': datetime(2001, 11, 25)},
    ]
    for data in departments_data:
        db.session.add(Department(**data))
    db.session.commit()
    print(f"Added {len(departments_data)} Departments.")

def add_sample_courses():
    """Adds 5 sample Course records, linked to departments."""
    print("Adding sample Courses...")
    # Assumes Department IDs are 1-5 from add_sample_departments
    courses_data = [
        {'department_id': 1, 'name': 'Bachelor of Technology in CS', 'code': 'B.Tech-CS', 'duration': 8},
        {'department_id': 2, 'name': 'Master of Science in EE', 'code': 'M.S-EE', 'duration': 4},
        {'department_id': 3, 'name': 'PhD in Mechanical Eng.', 'code': 'PhD-ME', 'duration': 6},
        {'department_id': 4, 'name': 'Bachelor of Science in Physics', 'code': 'B.Sc-PHY', 'duration': 6},
        {'department_id': 1, 'name': 'Diploma in Data Science', 'code': 'Dip-DS', 'duration': 4},
    ]
    for data in courses_data:
        db.session.add(Course(**data))
    db.session.commit()
    print(f"Added {len(courses_data)} Courses.")

def add_sample_subjects():
    """Adds 5 sample Subject records, linked to a course and department."""
    print("Adding sample Subjects...")
    # Assumes Course IDs are 1-5 and Department IDs are 1-5
    subjects_data = [
        {'course_id': 1, 'department_id': 1, 'name': 'Introduction to Programming', 'code': 'CS101', 'semester': 1, 'credits': 4},
        {'course_id': 1, 'department_id': 1, 'name': 'Data Structures', 'code': 'CS202', 'semester': 3, 'credits': 4},
        {'course_id': 2, 'department_id': 2, 'name': 'Advanced Circuit Theory', 'code': 'EE501', 'semester': 1, 'credits': 3},
        {'course_id': 4, 'department_id': 4, 'name': 'Quantum Mechanics', 'code': 'PHY301', 'semester': 5, 'credits': 5},
        {'course_id': 5, 'department_id': 1, 'name': 'Database Systems', 'code': 'DS103', 'semester': 2, 'credits': 3},
    ]
    for data in subjects_data:
        db.session.add(Subject(**data))
    db.session.commit()
    print(f"Added {len(subjects_data)} Subjects.")

def add_sample_students():
    """Adds 5 sample Student records."""
    print("Adding sample Students...")
    students_data = [
        {'first_name': 'Alice', 'last_name': 'Johnson', 'dob': date(2004, 8, 15), 'gender': 'Female', 'email': 'alice.j@uni.edu', 'phone': '9876543210', 'address': '123 Main St, City A'},
        {'first_name': 'Bob', 'last_name': 'Williams', 'dob': date(2003, 5, 20), 'gender': 'Male', 'email': 'bob.w@uni.edu', 'phone': '9876543211', 'address': '456 Oak Ave, City B'},
        {'first_name': 'Charlie', 'last_name': 'Brown', 'dob': date(2005, 1, 10), 'gender': 'Male', 'email': 'charlie.b@uni.edu', 'phone': '9876543212', 'address': '789 Pine Ln, City C'},
        {'first_name': 'Diana', 'last_name': 'Prince', 'dob': date(2003, 11, 25), 'gender': 'Female', 'email': 'diana.p@uni.edu', 'phone': '9876543213', 'address': '101 Side Rd, City A'},
        {'first_name': 'Eve', 'last_name': 'Moneypenny', 'dob': date(2004, 3, 5), 'gender': 'Female', 'email': 'eve.m@uni.edu', 'phone': '9876543214', 'address': '202 Center Blvd, City D'},
    ]
    for data in students_data:
        db.session.add(Student(**data))
    db.session.commit()
    print(f"Added {len(students_data)} Students.")

def add_sample_student_academics():
    """Adds 5 sample StudentAcademic records (marks/grades)."""
    print("Adding sample StudentAcademic records...")
    # Assumes Student IDs 1-5, Dept 1, Course 1, Subject IDs 1-5
    academics_data = [
        {'student_id': 1, 'department_id': 1, 'course_id': 1, 'subject_id': 1, 'semester': 1, 'marks': 85.5, 'grade': 'A'},
        {'student_id': 2, 'department_id': 1, 'course_id': 1, 'subject_id': 1, 'semester': 1, 'marks': 72.0, 'grade': 'B'},
        {'student_id': 3, 'department_id': 1, 'course_id': 1, 'subject_id': 2, 'semester': 3, 'marks': 91.2, 'grade': 'A+'},
        {'student_id': 4, 'department_id': 4, 'course_id': 4, 'subject_id': 4, 'semester': 5, 'marks': 65.8, 'grade': 'C'},
        {'student_id': 5, 'department_id': 1, 'course_id': 5, 'subject_id': 5, 'semester': 2, 'marks': 88.0, 'grade': 'A'},
    ]
    for data in academics_data:
        db.session.add(StudentAcademic(**data))
    db.session.commit()
    print(f"Added {len(academics_data)} StudentAcademic records.")

def add_sample_faculty():
    """Adds 5 sample Faculty records."""
    print("Adding sample Faculty...")
    faculty_data = [
        {'first_name': 'John', 'last_name': 'Smith', 'dob': date(1975, 1, 1), 'gender': 'Male', 'email': 'john.smith@uni.edu', 'phone': '9900112233', 'address': 'F1 Faculty Quarters'},
        {'first_name': 'Jane', 'last_name': 'Jones', 'dob': date(1980, 2, 2), 'gender': 'Female', 'email': 'jane.jones@uni.edu', 'phone': '9900112244', 'address': 'F2 Faculty Quarters'},
        {'first_name': 'Robert', 'last_name': 'Brown', 'dob': date(1968, 3, 3), 'gender': 'Male', 'email': 'robert.brown@uni.edu', 'phone': '9900112255', 'address': 'F3 Faculty Quarters'},
        {'first_name': 'Emily', 'last_name': 'Davis', 'dob': date(1990, 4, 4), 'gender': 'Female', 'email': 'emily.davis@uni.edu', 'phone': '9900112266', 'address': 'F4 Faculty Quarters'},
        {'first_name': 'Michael', 'last_name': 'Wilson', 'dob': date(1985, 5, 5), 'gender': 'Male', 'email': 'michael.w@uni.edu', 'phone': '9900112277', 'address': 'F5 Faculty Quarters'},
    ]
    for data in faculty_data:
        db.session.add(Faculty(**data))
    db.session.commit()
    print(f"Added {len(faculty_data)} Faculty members.")

def add_sample_faculty_assignments():
    """Adds 5 sample FacultyAssignment records (teaching load)."""
    print("Adding sample Faculty Assignments...")
    # Assumes Faculty IDs 1-5, Dept 1, Course 1, Subject IDs 1-5
    assignments_data = [
        {'faculty_id': 1, 'department_id': 1, 'course_id': 1, 'subject_id': 1, 'semester': 1}, # John Smith teaches CS101
        {'faculty_id': 2, 'department_id': 1, 'course_id': 1, 'subject_id': 2, 'semester': 3}, # Jane Jones teaches CS202
        {'faculty_id': 3, 'department_id': 2, 'course_id': 2, 'subject_id': 3, 'semester': 1}, # Robert Brown teaches EE501
        {'faculty_id': 4, 'department_id': 4, 'course_id': 4, 'subject_id': 4, 'semester': 5}, # Emily Davis teaches PHY301
        {'faculty_id': 5, 'department_id': 1, 'course_id': 5, 'subject_id': 5, 'semester': 2}, # Michael Wilson teaches DS103
    ]
    for data in assignments_data:
        db.session.add(FacultyAssignment(**data))
    db.session.commit()
    print(f"Added {len(assignments_data)} Faculty Assignments.")

def add_sample_books():
    """Adds 5 sample Book records."""
    print("Adding sample Books...")
    # Assumes Department IDs 1-5
    books_data = [
        {'title': 'The C Programming Language', 'author': 'Kernighan & Ritchie', 'isbn': '0131103628', 'copies': 5, 'department_id': 1},
        {'title': 'Digital Signal Processing', 'author': 'Proakis & Manolakis', 'isbn': '0131873740', 'copies': 3, 'department_id': 2},
        {'title': 'The Feynman Lectures on Physics', 'author': 'Feynman, Leighton, Sands', 'isbn': '046502494X', 'copies': 4, 'department_id': 4},
        {'title': 'Thermodynamics', 'author': 'Cengel and Boles', 'isbn': '007352932X', 'copies': 2, 'department_id': 3},
        {'title': 'Linear Algebra Done Right', 'author': 'Sheldon Axler', 'isbn': '3319110799', 'copies': 6, 'department_id': 5},
    ]
    for data in books_data:
        db.session.add(Book(**data))
    db.session.commit()
    print(f"Added {len(books_data)} Books.")

def add_sample_book_issues():
    """Adds 5 sample BookIssue records."""
    print("Adding sample Book Issues...")
    today = date.today()
    in_a_week = today + timedelta(days=7)
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    
    # Assumes Book IDs 1-5 and Student IDs 1-5
    issue_data = [
        {'book_id': 1, 'student_id': 1, 'issue_date': yesterday, 'return_date': in_a_week, 'actual_return_date': None}, # Currently issued
        {'book_id': 2, 'student_id': 2, 'issue_date': last_week, 'return_date': yesterday, 'actual_return_date': None}, # Overdue
        {'book_id': 3, 'student_id': 3, 'issue_date': last_week, 'return_date': in_a_week, 'actual_return_date': today}, # Returned on time
        {'book_id': 4, 'student_id': 4, 'issue_date': yesterday, 'return_date': in_a_week, 'actual_return_date': None}, # Currently issued
        {'book_id': 5, 'student_id': 5, 'issue_date': yesterday, 'return_date': in_a_week, 'actual_return_date': None}, # Currently issued
    ]
    for data in issue_data:
        db.session.add(BookIssue(**data))
    db.session.commit()
    print(f"Added {len(issue_data)} Book Issues.")

def add_sample_fees():
    """Adds 5 sample Fee records."""
    print("Adding sample Fees...")
    today = date.today()
    last_month = today.replace(day=1) - timedelta(days=1) # End of last month
    
    # Assumes Student IDs 1-5
    fees_data = [
        {'student_id': 1, 'amount': 50000.00, 'paid_amount': 50000.00, 'due_date': last_month, 'payment_date': last_month, 'status': 'Paid'},
        {'student_id': 2, 'amount': 50000.00, 'paid_amount': 25000.00, 'due_date': today + timedelta(days=15), 'payment_date': today, 'status': 'Partial Payment'},
        {'student_id': 3, 'amount': 50000.00, 'paid_amount': 0.00, 'due_date': today - timedelta(days=5), 'payment_date': None, 'status': 'Overdue'},
        {'student_id': 4, 'amount': 30000.00, 'paid_amount': 30000.00, 'due_date': today - timedelta(days=10), 'payment_date': today - timedelta(days=10), 'status': 'Paid'},
        {'student_id': 5, 'amount': 50000.00, 'paid_amount': 0.00, 'due_date': today + timedelta(days=30), 'payment_date': None, 'status': 'Pending'},
    ]
    for data in fees_data:
        db.session.add(Fee(**data))
    db.session.commit()
    print(f"Added {len(fees_data)} Fee records.")

def add_sample_events():
    """Adds 5 sample Event records."""
    print("Adding sample Events...")
    today = date.today()
    events_data = [
        {'title': 'Annual Robotics Workshop', 'description': 'Hands-on workshop for building autonomous robots.', 'event_type': 'Workshop', 'date': today + timedelta(days=10), 'location': 'CS Lab 3'},
        {'title': 'Cultural Fest: Rhapsody', 'description': 'Annual cultural event with dance, music, and drama.', 'event_type': 'Cultural', 'date': today + timedelta(days=30), 'location': 'Main Auditorium'},
        {'title': 'Guest Lecture: AI Ethics', 'description': 'Lecture on the ethical implications of artificial intelligence.', 'event_type': 'Seminar', 'date': today + timedelta(days=5), 'location': 'Seminar Hall A'},
        {'title': 'Inter-Department Cricket Tournament', 'description': 'Sports event for all departments.', 'event_type': 'Sports', 'date': today + timedelta(days=60), 'location': 'College Ground'},
        {'title': 'Mechanical Design Expo', 'description': 'Showcase of student projects in mechanical design.', 'event_type': 'Workshop', 'date': today + timedelta(days=15), 'location': 'ME Block'},
    ]
    for data in events_data:
        db.session.add(Event(**data))
    db.session.commit()
    print(f"Added {len(events_data)} Events.")

def add_sample_event_participants():
    """Adds 5 sample EventParticipant records."""
    print("Adding sample Event Participants...")
    # Assumes Event IDs 1-5, Student IDs 1-3, Faculty IDs 1-2
    participants_data = [
        {'event_id': 1, 'participant_type': 'student', 'participant_id': 1, 'role': 'Participant'},
        {'event_id': 2, 'participant_type': 'student', 'participant_id': 2, 'role': 'Participant'},
        {'event_id': 3, 'participant_type': 'faculty', 'participant_id': 1, 'role': 'Organizer'},
        {'event_id': 3, 'participant_type': 'faculty', 'participant_id': 2, 'role': 'Speaker'},
        {'event_id': 4, 'participant_type': 'student', 'participant_id': 3, 'role': 'Participant'},
    ]
    for data in participants_data:
        db.session.add(EventParticipant(**data))
    db.session.commit()
    print(f"Added {len(participants_data)} Event Participants.")

def populate_all_tables():
    """Runs all sample data population functions."""
    print("--- Starting Database Population ---")
    add_sample_users()
    add_sample_departments()
    add_sample_courses()
    add_sample_subjects()
    add_sample_students()
    add_sample_student_academics()
    add_sample_faculty()
    add_sample_faculty_assignments()
    add_sample_books()
    add_sample_book_issues()
    add_sample_fees()
    add_sample_events()
    add_sample_event_participants()
    print("--- Database Population Complete ---")

# --- Example of how to run this function in a Flask shell or script ---