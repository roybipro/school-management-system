import unittest

from school_management import Course, SchoolManagementSystem, Student, Teacher


class SchoolManagementSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sms = SchoolManagementSystem()
        self.student = Student("S1", "Alice")
        self.teacher = Teacher("T1", "Mr. Smith")
        self.course = Course("MATH101", "Mathematics")

        self.sms.add_student(self.student)
        self.sms.add_teacher(self.teacher)
        self.sms.add_course(self.course)

    def test_inheritance_and_polymorphism_profile(self) -> None:
        self.assertIn("Student", self.student.profile())
        self.assertIn("Teacher", self.teacher.profile())

    def test_enrollment_teacher_assignment_attendance_and_grades(self) -> None:
        self.sms.assign_teacher("MATH101", "T1")
        self.sms.enroll_student("MATH101", "S1")

        self.sms.record_attendance("MATH101", "S1", True)
        self.sms.record_attendance("MATH101", "S1", False)

        self.sms.record_grade("MATH101", "S1", 80)
        self.sms.record_grade("MATH101", "S1", 90)

        self.assertEqual(self.course.teacher_id, "T1")
        self.assertIn("MATH101", self.teacher.assigned_courses)
        self.assertIn("S1", self.course.student_ids)
        self.assertIn("MATH101", self.student.enrolled_courses)
        self.assertEqual(self.sms.attendance.percentage("MATH101", "S1"), 50.0)
        self.assertEqual(self.sms.grades.average("MATH101", "S1"), 85.0)

    def test_grade_validation(self) -> None:
        with self.assertRaises(ValueError):
            self.sms.record_grade("MATH101", "S1", 101)


if __name__ == "__main__":
    unittest.main()
