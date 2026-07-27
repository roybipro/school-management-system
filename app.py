"""A friendly Streamlit interface for the school management system."""

import json
from pathlib import Path

import streamlit as st


DATABASE_PATH = Path(__file__).with_name("school_database.json")


def load_database() -> dict:
    """Return a database with the expected keys, even for an empty file."""
    if not DATABASE_PATH.exists() or not DATABASE_PATH.read_text(encoding="utf-8").strip():
        return {"students": [], "teachers": []}
    with DATABASE_PATH.open(encoding="utf-8") as file:
        loaded = json.load(file)
    return {"students": loaded.get("students", []), "teachers": loaded.get("teachers", [])}


def save_database(database: dict) -> None:
    """Save safely so the existing records are not left half-written."""
    temporary_path = DATABASE_PATH.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(database, file, indent=4)
    temporary_path.replace(DATABASE_PATH)


def is_valid_email(email: str) -> bool:
    local, separator, domain = email.strip().partition("@")
    return bool(local and separator and "." in domain and not domain.startswith("."))


def student_average(student: dict) -> float:
    grades = student.get("grades", {})
    return sum(grades.values()) / len(grades) if grades else 0.0


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #f6f8fc; }
        [data-testid="stSidebar"] { background: #102a43; }
        [data-testid="stSidebar"] * { color: #f0f7ff; }
        .hero {
            padding: 2.1rem 2.3rem; border-radius: 22px; color: white;
            background: linear-gradient(115deg, #0b7285, #1864ab 56%, #364fc7);
            margin-bottom: 1.4rem;
        }
        .hero h1 { margin: 0; font-size: 2.25rem; }
        .hero p { margin: .5rem 0 0; color: #e7f5ff; font-size: 1.05rem; }
        .metric-card {
            background: white; padding: 1.1rem 1.25rem; border-radius: 16px;
            box-shadow: 0 5px 18px rgba(20, 45, 75, .07); min-height: 104px;
        }
        .metric-label { color: #62748a; font-size: .88rem; margin: 0; }
        .metric-value { color: #102a43; font-size: 1.75rem; font-weight: 700; margin: .2rem 0; }
        .section-title { color: #102a43; margin-top: 1.8rem; }
        div[data-testid="stForm"] { background: white; padding: 1.3rem; border-radius: 16px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)


def dashboard(database: dict) -> None:
    students, teachers = database["students"], database["teachers"]
    all_grades = [mark for student in students for mark in student.get("grades", {}).values()]
    average = sum(all_grades) / len(all_grades) if all_grades else 0
    page_header("School overview", "A clear snapshot of your school community and academic progress.")
    metrics = [("Enrolled students", len(students)), ("Teaching staff", len(teachers)), ("Average grade", f"{average:.1f}" if all_grades else "—")]
    columns = st.columns(3)
    for column, (label, value) in zip(columns, metrics):
        column.markdown(f"<div class='metric-card'><p class='metric-label'>{label}</p><p class='metric-value'>{value}</p></div>", unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>Student performance</h3>", unsafe_allow_html=True)
    if students:
        records = [{"Student": s["name"], "Roll no.": s["roll_no"], "Subjects": len(s.get("grades", {})), "Average": round(student_average(s), 1)} for s in students]
        st.bar_chart({record["Student"]: record["Average"] for record in records}, color="#1971c2")
        st.dataframe(records, hide_index=True, use_container_width=True)
    else:
        st.info("No students yet. Add your first student from the sidebar.")


def students_page(database: dict) -> None:
    page_header("Student directory", "Search, review, and manage student records in one place.")
    query = st.text_input("Search students", placeholder="Search by name, roll number, or email")
    students = database["students"]
    if query:
        term = query.lower().strip()
        students = [s for s in students if term in s["name"].lower() or term in s["roll_no"].lower() or term in s["email"].lower()]
    if not students:
        st.info("No matching students found." if query else "No students have been registered yet.")
        return
    rows = [{"Name": s["name"], "Roll no.": s["roll_no"], "Age": s["age"], "Email": s["email"], "Subjects": len(s.get("grades", {})), "Average": round(student_average(s), 1)} for s in students]
    st.dataframe(rows, hide_index=True, use_container_width=True)
    with st.expander("View a student profile"):
        selected_roll = st.selectbox("Select roll number", [s["roll_no"] for s in students])
        selected = next(s for s in students if s["roll_no"] == selected_roll)
        left, right = st.columns(2)
        left.write(f"**{selected['name']}**")
        left.caption(f"Roll no. {selected['roll_no']} · {selected['email']}")
        right.metric("Current average", f"{student_average(selected):.1f}")
        grades = selected.get("grades", {})
        st.dataframe([{"Subject": subject, "Mark": mark} for subject, mark in grades.items()], hide_index=True, use_container_width=True) if grades else st.caption("No grades recorded yet.")


def add_student_page(database: dict) -> None:
    page_header("Register a student", "Create a complete student profile in a few moments.")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Full name")
        first, second = st.columns(2)
        age = first.number_input("Age", min_value=3, max_value=120, value=12, step=1)
        roll_no = second.text_input("Roll number")
        email = st.text_input("Email address")
        submitted = st.form_submit_button("Register student", use_container_width=True)
    if submitted:
        if not all([name.strip(), roll_no.strip(), email.strip()]):
            st.error("Please complete every field.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif any(s["roll_no"].lower() == roll_no.strip().lower() for s in database["students"]):
            st.error("A student with this roll number already exists.")
        else:
            database["students"].append({"name": name.strip(), "age": int(age), "email": email.strip(), "roll_no": roll_no.strip(), "grades": {}})
            save_database(database)
            st.success(f"{name.strip()} has been registered successfully.")


def grades_page(database: dict) -> None:
    page_header("Gradebook", "Record subject results and keep every student’s progress up to date.")
    if not database["students"]:
        st.warning("Register a student before adding grades.")
        return
    choices = {f"{s['name']} — {s['roll_no']}": s for s in database["students"]}
    with st.form("grade_form", clear_on_submit=True):
        student_label = st.selectbox("Student", list(choices))
        subject, mark = st.columns(2)
        subject = subject.text_input("Subject")
        mark = mark.number_input("Mark", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
        submitted = st.form_submit_button("Save grade", use_container_width=True)
    if submitted:
        if not subject.strip():
            st.error("Please enter a subject.")
        else:
            student = choices[student_label]
            student.setdefault("grades", {})[subject.strip().title()] = float(mark)
            save_database(database)
            st.success(f"Saved {subject.strip().title()} for {student['name']}.")


def teachers_page(database: dict) -> None:
    page_header("Teaching staff", "Maintain staff profiles and the subjects they lead.")
    tab_directory, tab_register = st.tabs(["Directory", "Register teacher"])
    with tab_directory:
        teachers = database["teachers"]
        if teachers:
            rows = [{"Name": t["name"], "Employee ID": t["emp_id"], "Subject": t.get("Subject", t.get("subject", "—")), "Age": t["age"], "Email": t["email"]} for t in teachers]
            st.dataframe(rows, hide_index=True, use_container_width=True)
        else:
            st.info("No teachers have been registered yet.")
    with tab_register:
        with st.form("teacher_form", clear_on_submit=True):
            name = st.text_input("Full name")
            age, emp_id = st.columns(2)
            age = age.number_input("Age", min_value=18, max_value=120, value=25, step=1)
            emp_id = emp_id.text_input("Employee ID")
            email = st.text_input("Email address")
            subject = st.text_input("Primary subject")
            submitted = st.form_submit_button("Register teacher", use_container_width=True)
        if submitted:
            if not all([name.strip(), emp_id.strip(), email.strip(), subject.strip()]):
                st.error("Please complete every field.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif any(t["emp_id"].lower() == emp_id.strip().lower() for t in database["teachers"]):
                st.error("A teacher with this employee ID already exists.")
            else:
                database["teachers"].append({"name": name.strip(), "age": int(age), "email": email.strip(), "Subject": subject.strip().title(), "emp_id": emp_id.strip()})
                save_database(database)
                st.success(f"{name.strip()} has been registered successfully.")


def main() -> None:
    st.set_page_config(page_title="EduTrack | School Management", page_icon="🎓", layout="wide")
    inject_styles()
    database = load_database()
    with st.sidebar:
        st.title("🎓 EduTrack")
        st.caption("School management portal")
        st.divider()
        page = st.radio("Navigate", ["Dashboard", "Students", "Register student", "Gradebook", "Teachers"], label_visibility="collapsed")
        st.divider()
        st.caption("Records are saved securely to your local school database.")
    pages = {"Dashboard": dashboard, "Students": students_page, "Register student": add_student_page, "Gradebook": grades_page, "Teachers": teachers_page}
    pages[page](database)


if __name__ == "__main__":
    main()
