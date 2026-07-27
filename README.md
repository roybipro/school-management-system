# School Management System

EduTrack is a lightweight school management application built with Python and
Streamlit. It provides a simple dashboard for maintaining student records,
teacher records, and grades. All information is stored locally in a JSON file,
so no database server or account is required.

## Features

- Dashboard with total student and teacher counts, overall grade average, and a
  student-performance chart.
- Student directory with search by name, roll number, or email.
- Student registration with email and duplicate roll-number validation.
- Gradebook for adding or updating a student's mark for a subject.
- Teacher directory and registration with duplicate employee-ID validation.
- Local, safe record saving to `school_database.json`.

## Requirements

- Python 3.9 or newer
- pip

## Installation

Clone the repository, move into the project directory, and install the Python
dependency:

```bash
git clone <your-repository-url>
cd school-management-system
python -m pip install -r requirements.txt
```

## Run the application

Start the Streamlit web application with:

```bash
streamlit run app.py
```

Streamlit will display a local URL (normally `http://localhost:8501`). Open it
in your browser to use the application. Stop the server with `Ctrl+C` in the
terminal.

## Using EduTrack

1. Open **Register student** in the sidebar and enter the student's name, age,
   roll number, and email address.
2. Go to **Gradebook**, choose a student, then enter a subject and a mark from
   0 to 100. Saving a grade for an existing subject updates that subject's mark.
3. Use **Students** to search the directory and open an individual profile,
   including its grade history and calculated average.
4. Open **Teachers** to browse registered teachers or add a new teacher profile.
5. Return to **Dashboard** for a quick overview of school records and student
   performance.

## Data storage

The app reads from and writes to `school_database.json` in the project folder.
Keep a copy of this file if you want to back up your records. Its structure is:

```json
{
  "students": [
    {
      "name": "Student name",
      "age": 12,
      "email": "student@example.com",
      "roll_no": "101",
      "grades": { "Mathematics": 90.0 }
    }
  ],
  "teachers": [
    {
      "name": "Teacher name",
      "age": 30,
      "email": "teacher@example.com",
      "Subject": "Mathematics",
      "emp_id": "T-001"
    }
  ]
}
```

## Project structure

```text
.
├── app.py                 # Streamlit web application
├── main.py                # Original command-line OOP demonstration
├── school_database.json   # Local student and teacher data
├── requirements.txt       # Python dependency list
└── README.md
```

## Original CLI program

The original command-line demonstration is retained in `main.py`. Run it with:

```bash
python main.py
```
