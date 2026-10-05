import unittest 
from datetime import date
import husky as h  #necessary for functions written outside of the classes in the main file 
from husky import Course, Student, LinkedQueue, EnrollmentRecord, Node

#All testcases for Milestone 2, also includes a TestCourse class because of the addition of the attribute capacity and other methods. 
#Includes seperate TestCases for sorting algorithms under the class TestSortingAlgorithms. 

class TestCourse(unittest.TestCase):
    """Testcases handling updated attributes of Course class, as well as testing enrolling until capacity, adding students to waitlist, 
    and triggering waitlist promotion when a student drops a course.MP,MA"""
    def setUp(self):
        """Set up for obkects to be used in TestCourse testcases. MP"""
        self.course1 = Course("CSE2050", 3, 30) 
        self.course2 = Course("CSE1010", 3, 3)
        self.student1 = Student("STU00001", "Student_1")
        self.student2 = Student("STU00002", "Student_2")
        self.student3 = Student("STU00003", "Student_3")
        self.student4 = Student("STU00004", "Student_4")
        self.student5 = Student("STU00005", "Student_5")
        self.student6 = Student("STU00006", "Student_6")

    def test_init(self):
        """Testcase handling the initialization of a Course object, including attribute capacity.MP"""
        self.assertEqual(self.course1.course_code, "CSE2050")
        self.assertEqual(self.course1.credits, 3)
        self.assertEqual(self.course1.capacity, 30)

    def test_request_enroll(self):
        """Testcase handling the request_enroll method under the course class. MA"""
        self.course2.request_enroll(self.student1)
        self.course2.request_enroll(self.student2)
        self.course2.request_enroll(self.student3)
        self.course2.request_enroll(self.student4)
        self.assertEqual(self.course2.enrolled_roster[0].student, self.student1)
        self.assertEqual(self.course2.waitlist.dequeue(), self.student4) 

    def test_drop(self):
        """Testcase handling the drop method under the course class. MA"""
        self.course2.request_enroll(self.student1)
        self.course2.request_enroll(self.student2)
        self.course2.request_enroll(self.student3)
        self.assertEqual(self.course2.enrolled_roster[1].student, self.student2)
        self.course2.drop(self.student2.student_id)
        self.assertNotEqual(self.course2.enrolled_roster[1].student, self.student2)
        self.assertEqual(2, len(self.course2.enrolled_roster))
        self.course2.request_enroll(self.student4)
        self.course2.request_enroll(self.student5)
        self.course2.request_enroll(self.student6)
        self.assertEqual(self.course2.enrolled_roster[2].student, self.student4)
        self.course2.drop(self.student4.student_id)
        self.assertNotEqual(self.course2.enrolled_roster[2].student, self.student4)
        self.assertEqual(self.course2.enrolled_roster[2].student, self.student5)
        self.assertEqual(self.course2.waitlist.dequeue(), self.student6) 

    def test_sort_enrolled(self):
        """Testcase handling the sort_enrolled method under the course class. MA"""
        self.course1.request_enroll(self.student6, date(2027, 9, 1))
        self.course1.request_enroll(self.student1, date(2026, 9, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 4))
        self.course1.request_enroll(self.student2, date(2026, 9, 3))
        self.course1.request_enroll(self.student4, date(2026, 9, 4))
        self.course1.request_enroll(self.student5, date(2026, 12, 1))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("name","bubble")
        self.assertEqual(self.course1.enrolled_sorted_by,"name")
        for i in range(len(self.course1.enrolled_roster)):
            self.assertEqual(self.course1.enrolled_roster[i].student.name, test_sorted_list[i].name)
        self.course1.sort_enrolled("id","insertion")
        self.assertEqual(self.course1.enrolled_sorted_by,"id")
        for i in range(len(self.course1.enrolled_roster)):
            self.assertEqual(self.course1.enrolled_roster[i].student.student_id, test_sorted_list[i].student_id)
        self.course1.sort_enrolled("date", "bubble")
        self.assertEqual(self.course1.enrolled_sorted_by,"date")
        for i in range(len(self.course1.enrolled_roster)):
            self.assertEqual(self.course1.enrolled_roster[i].student, test_sorted_list[i])

class TestEnrollmentRecord(unittest.TestCase):
    """Testcases handling initialization of the EnrollmentRecord class, created objects from this class are to be stored inside of waitlist.
    MP"""
    def setUp(self):
        """Initializes student object and date to be used in following tests. MP"""
        self.student2 = Student("STU00002", "Student_2")
        self.test_date = date(2025, 3, 20)
    
    def test_init_record_with_date_string(self):
        """Test case for checking if a EnrollmentRecord object is initialized correctly with a date string. MP"""
        record = EnrollmentRecord(self.student2, "2025-03-20")
        self.assertEqual(record.enroll_date, self.test_date)

    def test_init_record_with_none(self):
        """Test case for checking if today's date is added when EnrollmentRecord.enroll_date is initialized as None. MP"""
        record = EnrollmentRecord(self.student2, None) 
        self.assertEqual(record.enroll_date, date.today())

    def test_init_record_raises_error(self):
        """Test case for checking if incorrectly formatted string raises an error in initialization. MP"""
        with self.assertRaises(ValueError):
            EnrollmentRecord(self.student2, "2025/03/20")

class TestNode(unittest.TestCase):
    """Structure used inside of the LinkedQueue ADT. MP"""
    def test_init(self):
        """Testcase handling correct initialization of the Node class strcuture."""
        self.node1 = Node(4) 
        self.assertEqual(self.node1.data, 4)
        self.assertEqual(self.node1.next, None)

class TestLinkedQueue(unittest.TestCase):
    """ADT structure used to handle waitlist behavior for students unable to register for a course with full capacity. MP"""
    def setUp(self):
        """Set up for objects to be used in testcases of LinkedQueue."""
        self.empty_queue = LinkedQueue()
        self.single_item = LinkedQueue()
        self.single_item.enqueue("Student_1")
        self.multiple_items = LinkedQueue()
        for student in ["Student_1", "Student_2", "Student_3"]:
            self.multiple_items.enqueue(student)
    
    def test_init(self):
        """Testcase handling correct initialization of LinkedQueue. MP"""
        queue = LinkedQueue()
        self.assertEqual(queue.is_empty(), True)
        self.assertEqual(len(queue), 0)
        self.assertEqual(queue.head, None)
        self.assertEqual(queue.tail, None)
        self.assertEqual(queue.size, 0)

    def test_enqueue(self):
        """Testcase checking correct behavior of enqueue() in LinkedQueue. MP"""
        queue = LinkedQueue() 
        queue.enqueue("Student_1")
        self.assertEqual(queue.head.data, "Student_1")
        self.assertEqual(queue.tail.data, "Student_1")
        self.assertEqual(len(queue), 1)
        queue.enqueue("Student_2")
        self.assertEqual(queue.head.data, "Student_1")
        self.assertEqual(queue.tail.data, "Student_2")
        self.assertEqual(len(queue), 2)

    def test_dequeue(self):
        """Testcase checking correct behavior of dequeue() in LinkedQueue. MP"""
        queue = LinkedQueue()
        with self.assertRaises(ValueError):
            queue.dequeue()
        queue_single = LinkedQueue()
        queue_single.enqueue("Student_1")
        self.assertEqual(len(queue_single), 1)
        queue_single.dequeue()
        self.assertEqual(len(queue_single), 0)
        self.assertEqual(queue_single.is_empty(), True)

    def test_isEmpty(self):
        """Testcase checking correct behavior of isEmpty() in LinkedQueue, returning True/False. MP"""
        self.assertEqual(self.empty_queue.is_empty(), True) 
        self.assertEqual(self.single_item.is_empty(), False) 
        self.assertEqual(self.multiple_items.is_empty(), False) 

    def test_len(self):
        """Testcase checking correct behavior of __len__ dunder method, returning size attribute of LinkedQueue. MP"""
        self.assertEqual(len(self.empty_queue), 0) 
        self.assertEqual(len(self.empty_queue), self.empty_queue.size)
        self.assertEqual(len(self.single_item), 1)
        self.assertEqual(len(self.single_item), self.single_item.size)
        self.assertEqual(len(self.multiple_items), 3)
        self.assertEqual(len(self.multiple_items), self.multiple_items.size)


class TestSortingAlgorithms(unittest.TestCase):
    """Testcases handling all sorting algorithms which were implemented, different variations of bubble sort and insertion sort which
    search by different keys are also tested. MA"""
    def setUp(self):
        self.course1 = Course("CSE2050", 3, 30)
        self.student1 = Student("STU00001", "Student_1")
        self.student2 = Student("STU00002", "Student_2")
        self.student3 = Student("STU00003", "Student_3")
        self.student4 = Student("STU00004", "Student_4")
        self.student5 = Student("STU00005", "Student_5")
        self.student6 = Student("STU00006", "Student_6")

    
    def test_recursive_binary_search(self):
        """Testcases handling the recursive_binary_search function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        self.course1.sort_enrolled("id","insertion")
        self.assertTrue(h.recursive_binary_search(self.course1.enrolled_roster, self.student3.student_id, 0, len(self.course1.enrolled_roster)))


    def test_bubble_sort_student_id(self):
        """Testcases handling the bubble_sort_student_id function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("id","bubble")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.student_id, test_sorted_list[i].student_id)


    def test_bubble_sort_name(self):
        """Testcases handling the bubble_sort_name function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("name", "bubble")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.name, test_sorted_list[i].name)


    def test_bubble_sort_date(self):
        """Testcases handling the bubble_sort_date function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("date","bubble")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student, test_sorted_list[i])

    def test_insertion_sort_student_id(self):
        """Testcases handling the insertion_sort_student_id function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("id","insertion")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.student_id, test_sorted_list[i].student_id)


    def test_insertion_sort_name(self):
        """Testcases handling the insertion_sort_name function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("name","insertion")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.name, test_sorted_list[i].name)


    def test_insertion_sort_date(self):
        """Testcases handling the insertion_sort_date function. MA"""
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
        test_sorted_list = [self.student1, self.student2, self.student3, self.student4, self.student5, self.student6]
        self.course1.sort_enrolled("date","insertion")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student, test_sorted_list[i])

unittest.main()