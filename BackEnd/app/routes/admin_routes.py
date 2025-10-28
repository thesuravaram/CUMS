


# from flask import Blueprint, request, jsonify
# from app.services.admin_services import (
#     get_all_students, get_student_detail, create_student, update_student, delete_student,
#     get_all_faculty, get_faculty_detail, create_faculty, update_faculty, delete_faculty,
#     get_all_books, get_all_book_issues, add_book, issue_book, return_book,
#     get_all_fees,
#     get_all_events, get_event_detail, create_event, update_event, delete_event
# )


# admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# # ==============================
# # Students
# # ==============================




# @admin_bp.route("/students", methods=["GET"])
# def students():
#     return jsonify(get_all_students()), 200


# @admin_bp.route("/students/<int:student_id>", methods=["GET"])
# def student_detail_route(student_id):
#     return jsonify(get_student_detail(student_id)), 200


# @admin_bp.route("/create/students", methods=["POST"])
# def create_student_route():
#     data = request.json
#     return jsonify(create_student(data)), 201


# @admin_bp.route("/update//students/<int:student_id>", methods=["PUT"])
# def update_student_route(student_id):
#     data = request.json
#     return jsonify(update_student(student_id, data)), 200


# @admin_bp.route("/delete/students/<int:student_id>", methods=["DELETE"])
# def delete_student_route(student_id):
#     return jsonify(delete_student(student_id)), 200


# app/routes/admin_routes.py

from flask import Blueprint, request, jsonify, send_file # Added send_file
from app.services.admin_services import (
    get_all_students, get_student_detail, update_student, delete_student,
    get_all_faculty, get_faculty_detail, create_faculty, update_faculty, delete_faculty,
    get_all_books, get_all_book_issues, add_book, issue_book, return_book,
    get_all_fees,
    get_all_events, get_event_detail, create_event, update_event, delete_event,
    
    # NEW IMPORTS FOR DOCUMENT HANDLING
    create_student_with_documents, # NEW function for POST
    get_student_documents,         # NEW function for listing documents
    download_student_document      # NEW function for downloading
)

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# ==============================
# Students
# ==============================

@admin_bp.route("/students", methods=["GET"])
def students():
    return jsonify(get_all_students()), 200

# The detail route will now fetch and include document metadata
@admin_bp.route("/students/<int:student_id>", methods=["GET"])
def student_detail_route(student_id):
    # get_student_detail service function is updated to include document list
    return jsonify(get_student_detail(student_id)), 200


# --- REPLACED: CREATE ROUTE TO HANDLE MULTIPART FORM DATA ---
@admin_bp.route("/create/students", methods=["POST"])
def create_student_route():
    """
    Creates a student and stores any uploaded documents.
    Expects student fields in request.form and file(s) in request.files.
    """
    # Get all non-file fields (name, email, etc.)
    data = request.form.to_dict() 
    # Get all files named 'documents' from the form
    files = request.files.getlist('documents') 
    
    result, status_code = create_student_with_documents(data, files)
    
    return jsonify(result), status_code
# -----------------------------------------------------------


@admin_bp.route("/update/students/<int:student_id>", methods=["PUT"])
def update_student_route(student_id):
    data = request.json
    return jsonify(update_student(student_id, data)), 200


@admin_bp.route("/delete/students/<int:student_id>", methods=["DELETE"])
def delete_student_route(student_id):
    return jsonify(delete_student(student_id)), 200

# ==============================
# Student Documents (NEW ROUTES)
# ==============================

@admin_bp.route("/students/<int:student_id>/documents", methods=["GET"])
def list_student_documents_route(student_id):
    """Lists all document metadata for a specific student from MongoDB."""
    return jsonify(get_student_documents(student_id)), 200

@admin_bp.route("/students/documents/download/<doc_id>", methods=["GET"])
def download_student_document_route(doc_id):
    """Downloads a specific document by its UUID from Cassandra."""
    file_data, file_name = download_student_document(doc_id)
    
    if file_data is None:
        return jsonify({"error": f"Document ID {doc_id} not found"}), 404
    
    # Use BytesIO to stream file data back to the client
    from io import BytesIO
    return send_file(
        BytesIO(file_data),
        download_name=file_name,
        as_attachment=True,
        mimetype='application/octet-stream'
    )

# ... (Rest of Faculty, Library, Fees, Events routes remain the same) ...

# ==============================
# Faculty
# ==============================
@admin_bp.route("/faculty", methods=["GET"])
def faculty():
    return jsonify(get_all_faculty()), 200


@admin_bp.route("/faculty/<int:faculty_id>", methods=["GET"])
def faculty_detail_route(faculty_id):
    return jsonify(get_faculty_detail(faculty_id)), 200


@admin_bp.route("/create/faculty", methods=["POST"])
def create_faculty_route():
    data = request.json
    return jsonify(create_faculty(data)), 201


@admin_bp.route("/update/faculty/<int:faculty_id>", methods=["PUT"])
def update_faculty_route(faculty_id):
    data = request.json
    return jsonify(update_faculty(faculty_id, data)), 200


@admin_bp.route("/delete/faculty/<int:faculty_id>", methods=["DELETE"])
def delete_faculty_route(faculty_id):
    return jsonify(delete_faculty(faculty_id)), 200


# ==============================
# Library
# ==============================
@admin_bp.route("/library/books", methods=["GET"])
def books():
    return jsonify(get_all_books()), 200


@admin_bp.route("/add/library/books", methods=["POST"])
def add_book_route():
    data = request.json
    return jsonify(add_book(data)), 201


@admin_bp.route("/library/issues", methods=["GET"])
def book_issues():
    return jsonify(get_all_book_issues()), 200


@admin_bp.route("/library/issues", methods=["POST"])
def issue_book_route():
    data = request.json
    return jsonify(issue_book(data)), 201


@admin_bp.route("/library/issues/<int:issue_id>", methods=["PUT"])
def return_book_route(issue_id):
    data = request.json
    return jsonify(return_book(issue_id, data)), 200


# ==============================
# Fees
# ==============================
@admin_bp.route("/fees", methods=["GET"])
def fees():
    return jsonify(get_all_fees()), 200


# ==============================
# Events
# ==============================
@admin_bp.route("/events", methods=["GET"])
def events():
    return jsonify(get_all_events()), 200


@admin_bp.route("/events/<int:event_id>", methods=["GET"])
def event_detail_route(event_id):
    return jsonify(get_event_detail(event_id)), 200


@admin_bp.route("/events", methods=["POST"])
def create_event_route():
    data = request.json
    return jsonify(create_event(data)), 201


@admin_bp.route("/update/events/<int:event_id>", methods=["PUT"])
def update_event_route(event_id):
    data = request.json
    return jsonify(update_event(event_id, data)), 200


@admin_bp.route("/delete/events/<int:event_id>", methods=["DELETE"])
def delete_event_route(event_id):
    return jsonify(delete_event(event_id)), 200
