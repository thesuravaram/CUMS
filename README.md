# Centralized University Database System (CUMS)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Cassandra](https://img.shields.io/badge/Cassandra-1287B1?style=for-the-badge&logo=apachecassandra&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

CUMS is a modern, unified platform designed to solve the data fragmentation problem in universities. It replaces traditional, siloed systems (for admissions, finance, academics) with a **single source of truth** to streamline operations, enhance the student experience, and provide powerful data analytics for institutional leaders.

This project is submitted in partial fulfillment of the requirements for the M.Tech in Data Science at Manipal Institute of Technology (MIT).

---

## 📖 Table of Contents
- [The Problem](#❗-the-problem)
- [Core Objectives](#🎯-core-objectives)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Features & Modules](#-features--modules)
- [Database Schema](#-database-schema)
- [Getting Started](#-getting-started)
- [Results & Impact](#-results--impact)
- [Conclusion](#-conclusion)
- [Future Scope](#-future-scope)

---

## ❗ The Problem

> Modern universities traditionally operate within a fragmented technological ecosystem, utilizing disparate, non-integrated software systems for critical administrative and academic functions—including admissions, student information systems (SIS), financial management, and learning management systems (LMS).
>
> This decentralized data architecture creates significant operational inefficiencies, characterized by data redundancy, a high incidence of manual entry errors, and a lack of data integrity across departments. The resulting data silos prevent the formation of a holistic, 360-degree view of the student, leading to a poor and fragmented user experience.
>
> The core problem is the **absence of a single, centralized platform** that can unify data, streamline processes, and provide a single source of truth for all institutional stakeholders.

## 🎯 Core Objectives

1.  **Unify All Data:** Create one central database for all departments.
2.  **Automate Operations:** Eliminate manual data entry and repetitive tasks.
3.  **Simplify User Access:** Provide one portal and one login for everyone.
4.  **Improve Reporting:** Give leaders accurate, real-time data for better decisions.

## 🛠️ Tech Stack & Architecture

### Architectural Overview

| Layer | Description |
| :--- | :--- |
| **Frontend (Client Layer)** | Developed using **React Native** ensuring responsiveness and dynamic UI interactions. |
| **Backend (Application Layer)** | Built using **FastAPI**, leveraging asynchronous I/O for high-performance REST API handling. |
| **Database Layer** | Used **PostgreSQL** for structured data, complemented by **Cassandra** for distributed storage and **MongoDB** (optional future use) for caching and analytics. |
| **Integration Layer** | Enables seamless integration of all university modules into a centralized database, ensuring real-time data synchronization. |
| **Analytics Layer** | Provides comprehensive analysis and visualization of student grades, attendance, and performance metrics. |

### Tools and Technologies

| Category | Tools / Frameworks | Purpose |
| :--- | :--- | :--- |
| **Programming Languages** | Python, JavaScript, CSS, HTML, Node.js | Core development |
| **Backend** | FastAPI, SQLAlchemy | API logic, ORM, and migrations |
| **Frontend** | React Native, Material UI, Tailwind CSS | UI, charts, and routing |
| **Database** | PostgreSQL, MongoDB, Cassandra | Transactional data management |
| **Task Scheduler** | APScheduler | Automated alerts |
| **Version Control** | Git, GitHub | Collaboration and code management |
| **Containerization** | Docker | Cross-platform environment setup |

---

## ✨ Features & Modules

* **📊 Dashboard**
    * Provides a real-time summary of student enrollment, attendance, and performance.
    * Displays key metrics for faculty, departments, and courses.
    * Offers interactive visualizations for data insights.

* **🧑‍🎓 Student Management**
    * Allows adding, updating, deleting, and viewing student details.
    * Supports dynamic search and filtering by student name, ID, or department.

* **👩‍🏫 Faculty Management**
    * Manages faculty profiles, subject assignments, and schedules.
    * Tracks performance, workload, and attendance records.

* **📚 Course & Department Management**
    * Handles creation, modification, and deletion of courses and departments.
    * Maintains course-faculty-student relationships.

* **💳 Fee Management**
    * Tracks student fee payments, dues, and financial transactions.
    * Generates digital receipts and financial summaries.
    * Sends automated reminders for pending or overdue payments.

* **📖 Library Management**
    * Maintains a catalog of available books and digital resources.
    * Tracks book issuance, returns, and due dates.
    * Generates alerts for overdue books and manages fine collections.

* **🎉 Event Management**
    * Organizes academic, cultural, and sports events.
    * Manages participant lists, schedules, and performance reports.

* **🔔 Alert & Notification System**
    * Sends real-time notifications for important academic updates.
    * Issues alerts for fee dues, attendance shortages, and exam schedules (e.g., Red = Urgent, Yellow = Reminder).

* **📈 Analytics & Reporting**
    * Provides detailed analysis of student grades, attendance, and performance trends.
    * Generates department-wise and faculty-wise performance reports.

* **🤖 IoT & Automation Layer (Planned)**
    * Integrates with biometric and RFID systems for real-time attendance tracking.
    * Automates data updates in the centralized database from connected devices.

---

## 🗄️ Database Schema

<details>
<summary>Click to view database tables</summary>

* **users** (id, email, password_hash, role)
* **departments** (id, name, code, created_at)
* **courses** (id, department_id, name, code, duration, created_at)
* **subjects** (id, course_id, department_id, name, code, semester, credits)
* **students** (id, first_name, last_name, dob, gender, email, phone, address, created_at)
* **student_academics** (id, student_id, department_id, course_id, subject_id, semester, marks, grade)
* **faculty** (id, first_name, last_name, dob, gender, email, phone, address, created_at)
* **faculty_assignments** (id, faculty_id, department_id, course_id, subject_id, semester)
* **books** (id, title, author, isbn, copies, department_id)
* **book_issues** (id, book_id, student_id, issue_date, return_date, actual_return_date)
* **fees** (id, student_id, amount, paid_amount, due_date, payment_date, status)
* **events** (id, title, description, event_type, date, location, created_at)
* **event_participants** (id, event_id, participant_type, participant_id, role, registered_at)

</details>

---

## 🚀 Getting Started

Instructions to get a local copy up and running.

### Prerequisites

* Python 3.9+
* Node.js & npm
* PostgreSQL
* Docker (Optional, but recommended for easier setup)

### 1. Clone the Repository

bash
git clone [https://github.com/thesuravaram/CUMS.git](https://github.com/thesuravaram/CUMS.git)
cd CUMS

### 2. Backend Setup (FastAPI)

# Navigate to the backend directory (assuming 'backend/')
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your .env file with PostgreSQL credentials
# (You may need to create a 'config.py' or '.env' file)
# Example:
# DATABASE_URL="postgresql://user:password@localhost/cums_db"

# Run the database migrations (if using Alembic/SQLAlchemy)
# alembic upgrade head

# Run the API server
uvicorn main:app --reload

### 3. Frontend Setup (React Native)

# Navigate to the frontend directory (assuming 'frontend/')
cd frontend

# Install dependencies
npm install

# Start the Metro bundler
npm start

# Run on Android or iOS
npm run android
# or
npm run ios
