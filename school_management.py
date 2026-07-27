from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Set


class Person(ABC):
    """Abstract base class for all people in the school."""

    def __init__(self, person_id: str, name: str) -> None:
        self._person_id = person_id
        self._name = name

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def role(self) -> str:
        """Return role-specific text."""

    def profile(self) -> str:
        return f"{self.name} ({self.person_id}) - {self.role()}"


class Student(Person):
    def __init__(self, person_id: str, name: str) -> None:
        super().__init__(person_id, name)
        self._enrolled_courses: Set[str] = set()

    @property
    def enrolled_courses(self) -> Set[str]:
        return set(self._enrolled_courses)

    def enroll(self, course_code: str) -> None:
        self._enrolled_courses.add(course_code)

    def role(self) -> str:
        return "Student"


class Teacher(Person):
    def __init__(self, person_id: str, name: str) -> None:
        super().__init__(person_id, name)
        self._assigned_courses: Set[str] = set()

    @property
    def assigned_courses(self) -> Set[str]:
        return set(self._assigned_courses)

    def assign_course(self, course_code: str) -> None:
        self._assigned_courses.add(course_code)

    def role(self) -> str:
        return "Teacher"


@dataclass
class Course:
    code: str
    name: str
    teacher_id: str | None = None
    student_ids: Set[str] = field(default_factory=set)


class AttendanceManager:
    """Handles attendance tracking by course and student."""

    def __init__(self) -> None:
        self._attendance: Dict[str, Dict[str, List[bool]]] = {}

    def record(self, course_code: str, student_id: str, present: bool) -> None:
        self._attendance.setdefault(course_code, {}).setdefault(student_id, []).append(present)

    def percentage(self, course_code: str, student_id: str) -> float:
        records = self._attendance.get(course_code, {}).get(student_id, [])
        if not records:
            return 0.0
        return (sum(records) / len(records)) * 100


class GradeManager:
    """Handles grade tracking by course and student."""

    def __init__(self) -> None:
        self._grades: Dict[str, Dict[str, List[float]]] = {}

    def add_grade(self, course_code: str, student_id: str, score: float) -> None:
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self._grades.setdefault(course_code, {}).setdefault(student_id, []).append(score)

    def average(self, course_code: str, student_id: str) -> float:
        scores = self._grades.get(course_code, {}).get(student_id, [])
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


class SchoolManagementSystem:
    """Coordinates students, teachers, courses, attendance, and grades."""

    def __init__(self) -> None:
        self.students: Dict[str, Student] = {}
        self.teachers: Dict[str, Teacher] = {}
        self.courses: Dict[str, Course] = {}
        self.attendance = AttendanceManager()
        self.grades = GradeManager()

    def add_student(self, student: Student) -> None:
        self.students[student.person_id] = student

    def add_teacher(self, teacher: Teacher) -> None:
        self.teachers[teacher.person_id] = teacher

    def add_course(self, course: Course) -> None:
        self.courses[course.code] = course

    def assign_teacher(self, course_code: str, teacher_id: str) -> None:
        course = self.courses[course_code]
        teacher = self.teachers[teacher_id]
        course.teacher_id = teacher_id
        teacher.assign_course(course_code)

    def enroll_student(self, course_code: str, student_id: str) -> None:
        course = self.courses[course_code]
        student = self.students[student_id]
        course.student_ids.add(student_id)
        student.enroll(course_code)

    def record_attendance(self, course_code: str, student_id: str, present: bool) -> None:
        self.attendance.record(course_code, student_id, present)

    def record_grade(self, course_code: str, student_id: str, score: float) -> None:
        self.grades.add_grade(course_code, student_id, score)
