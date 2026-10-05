import unittest
from husky import Course, Student, University 


class TestCourse(unittest.TestCase):
    """Contains all testcases for the initialization and methods contained with Course class."""
    def setUp(self):
        """Contains all objects initialized under each class to test. MP"""
        self.course_obj1 = Course("CSE2050", 3)

    def test_init(self):
        """Tests initialization methods under the Course class. MP"""
        self.assertEqual(self.course_obj1.course_code, "CSE2050")
        self.assertEqual(self.course_obj1.credits, 3)
        self.assertEqual(self.course_obj1.students, [])

    def test_add_student(self):
        """Tests if the student object in the parameter of the add_student method was added
        to the students list, also tests if duplicate objects are prevented from being added
        to the student roster. MP"""
        obj = Course("CSE2050", 3, ["Michael"])
        obj.add_student("Melissa")
        self.assertEqual(obj.students[0], "Melissa")
        with self.assertRaises(NameError):
            obj.add_student("Melissa")

    def test_get_student_count(self):
        """Tests if the number of students returned is the same as what is stored in
        the length of the students list. MP"""
        self.assertEqual(len(self.course_obj1.students), 0)

class TestStudent(unittest.TestCase):
    """Contains all testcases for initialization and methods with the Student class."""
    def setUp(self):
        """Contains all objects initialized under Student class for testcases."""
        self.student_obj1 = Student("STU00001","Chris Walker")
        self.student_obj2 = Student("STU00002", "Mike Arcari", {})
        self.course_obj1 = Course("CSE2050", 3)
        self.course_obj2 = Course("ANTH1000", 3)
    
    def test_init(self):
        """Tests initialization within the Student class. MP"""
        self.assertEqual(self.student_obj1.student_id, "STU00001")
        self.assertEqual(self.student_obj1.name, "Chris Walker")
        self.assertEqual(self.student_obj1.courses, {})

    def test_enroll(self):
        """Tests that a new course a student is enrolled in is added to dictionary course. MP"""
        self.student_obj1.enroll(self.course_obj1, "B")
        self.assertIn(self.student_obj1.courses[self.course_obj1], "B")
        self.assertEqual(len(self.student_obj1.courses), 1)

    def test_calculate_gpa(self):
        """Tests that gpa is calculated correctly given courses and associated grades/credits.
        MP"""
        self.student_obj1.enroll(self.course_obj1, "B")
        self.student_obj1.enroll(self.course_obj2, "A-")
        self.assertEqual(self.student_obj1.calculate_gpa(), 3.35)

    def test_get_courses(self):
        """Tests that a list containing a student courses is correctly returned. MP"""
        self.student_obj1.enroll(self.course_obj1, "B")
        self.assertEqual(self.student_obj1.get_courses(), ["CSE2050"])


class TestUniversity(unittest.TestCase):
    """Contains all test cases for the University class, our central manager. MP"""
    def setUp(self):
        """Includes creation of student and course objects to be used in unittests."""
        self.student1 = Student("STU00004", "Harlow")
        self.student2 = Student("STU00005", "Sebastian")
        self.course1 = Course("CHEM1127Q", 4)
        self.course2 = Course("CSE2301", 4)
    
    def test_init(self):
        """Tests empty initialization of the University class and also with items inside the
        students and courses dictionaries. MP"""
        uconn = University()
        self.assertEqual(uconn.students, {})
        self.assertEqual(uconn.courses, {})
        
        students_dict = {
            "STU00004": self.student1,
            "STU00005": self.student2
        }
        uni1 = University(students=students_dict)
        self.assertEqual(len(uni1.students), 2)
        self.assertEqual(uni1.students["STU00004"], self.student1)
        self.assertEqual(uni1.students["STU00005"], self.student2)
        
        courses_dict = {
            "CHEM1127Q": self.course1,
            "CSE2301": self.course2
        }
        uni2 = University(courses=courses_dict)
        self.assertEqual(len(uni2.courses), 2)
        self.assertEqual(uni2.courses["CHEM1127Q"], self.course1)
        self.assertEqual(uni2.courses["CSE2301"], self.course2)

    def test_add_course(self):
        """Tests adding a course to University object and also tests adding a duplicate 
        course. MP"""
        uconn = University()
        course1 = uconn.add_course("CHEM1127Q", 4)
        self.assertIn("CHEM1127Q", uconn.courses)
        self.assertEqual(course1.course_code, "CHEM1127Q")
        self.assertEqual(course1.credits, 4)
        
        #Testing adding duplicate courses.
        with self.assertRaises(KeyError):
            uconn.add_course("CHEM1127Q", 3)

    def test_add_student(self):
        """Tests adding a student to University object and also tests adding a duplicate
        student. Also tests if correct student ID format is used. MP"""
        uconn = University()
        student1 = uconn.add_student("STU00005", "Sebastian") 
        self.assertIn("STU00005", uconn.students)
        self.assertEqual(student1.student_id, "STU00005")
        self.assertEqual(student1.name, "Sebastian")
        
        #Testing adding duplicate studen IDs and also incorrect ID formats.
        with self.assertRaises(KeyError):
            uconn.add_student("STU00005", "Mikayla")
        with self.assertRaises(KeyError):
            uconn.add_student("UCD00005", "Mikayla")
        with self.assertRaises(ValueError):
            uconn.add_student("STU0000005", "Mikayla")

    def test_get_student(self):
        """Tests getting the student object from the student ID. MP"""
        uconn = University()
        uconn.add_student("STU00006", "Alice")
        student = uconn.get_student("STU00006")
        self.assertEqual(student.name, "Alice")
        self.assertEqual(student.student_id, "STU00006")
        #Asserts that None is returned if there is no student object matching that ID.
        self.assertEqual(uconn.get_student("STU00007"), None)
        
        #Tests if student ID is correct length and format.
        with self.assertRaises(ValueError):
            uconn.get_student("STU000006")
        with self.assertRaises(KeyError):
            uconn.get_student("UCD00006")

    def test_get_course(self):
        """Tests getting the course object from the course code. MP"""
        uconn = University()
        uconn.add_course("CHEM1127Q", 4)
        course = uconn.get_course("CHEM1127Q")
        self.assertEqual(course.course_code, "CHEM1127Q")
        self.assertEqual(course.credits, 4)
        #Tests to see if error is raised when invalid course code is given.
        with self.assertRaises(KeyError):
            uconn.get_course("CSE2891")

    def test_get_course_enrollment(self):
        """Tests getting the amount of students enrolled in a course. MA"""
        uconn = University()
        uconn.add_student("STU00004", "Harlow")
        uconn.add_student("STU00005", "Sebastian")
        uconn.add_student("STU00006", "Jake")
        uconn.add_course("CHEM1127Q", 4)
        uconn.get_course("CHEM1127Q").add_student("STU00004")
        uconn.get_course("CHEM1127Q").add_student("STU00005")
        uconn.get_course("CHEM1127Q").add_student("STU00006")
        self.assertIn("STU00004", uconn.students)
        self.assertIn("STU00005", uconn.students)
        self.assertIn("STU00006", uconn.students)
        self.assertIn("CHEM1127Q", uconn.courses)
        self.assertEqual(uconn.get_course_enrollment("CHEM1127Q"), 3)

        with self.assertRaises(KeyError):
            uconn.get_course_enrollment("5")


    def test_get_students_in_course(self):
        """Tests getting a list of students enrolled in a course. MA"""
        uconn = University()
        student1 = uconn.add_student("STU00004", "Harlow")
        student2 = uconn.add_student("STU00005", "Sebastian")
        student3 = uconn.add_student("STU00006", "Jake")
        course1 = uconn.add_course("CHEM1127Q", 4)
        student1.enroll(course1,"A")
        student2.enroll(course1,"A")
        student3.enroll(course1,"A")
        self.assertIn("STU00004", uconn.students)
        self.assertIn("STU00005", uconn.students)
        self.assertIn("STU00006", uconn.students)
        self.assertIn("CHEM1127Q", uconn.courses)
        #print(uconn.courses.keys())
        self.assertEqual(uconn.get_students_in_course("CHEM1127Q"), ["STU00004", "STU00005", "STU00006"])


"""Executes all tests within the testcase file."""
unittest.main()