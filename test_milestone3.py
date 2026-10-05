import unittest 
from husky import Course, HashMap, ListMapping, Course, Student
from datetime import date 

#All testcases for Milestone 3, includes the 3 main classes with the testcases described in 
# Milestone 3. An additional testcase class was added for ListMapping, mainly for the get/put method.

class TestHashmap(unittest.TestCase):
    """Class which holds all testcases relevant to testing correct collision handling and rehashing behavior in a Hashmap. MP"""
    def setUp(self):
        """Holds a Hashmap object to be used in each test. MP"""
        self.hashmap = HashMap(size=8)  # hash(key) % 8
        #use for rehash testcase
        self.smallhashmap = HashMap(size=4) # hash(key) % 4 
    
    def test_rehash(self):
        """Testcase to handle rehashing when load factor of the hash table is reached. MP"""
        self.smallhashmap.put(0, "value1")
        self.smallhashmap.put(4, "value2")
        self.assertEqual(self.smallhashmap.get(0), "value1")
        self.assertEqual(self.smallhashmap.get(4), "value2")
        bucket0 = self.smallhashmap._buckets[0]
        self.assertEqual(len(bucket0), 2)
        #triggering rehash
        self.smallhashmap.put(2, "value3")
        self.smallhashmap.put(3, "value4")
        bucket0 = self.smallhashmap._buckets[0]
        bucket2 = self.smallhashmap._buckets[2]
        bucket3 = self.smallhashmap._buckets[3]
        bucket4 = self.smallhashmap._buckets[4]
        self.assertEqual(len(bucket0), 1)
        self.assertEqual(len(bucket2), 1)
        self.assertEqual(len(bucket3), 1)
        self.assertEqual(len(bucket4), 1)
    
    def test_collision_handling(self):
        """Testcase to demonstrate correct collision handling,
        multiple keys per bucket work correctly. MP"""
        #Tests for same bucket collision
        self.hashmap.put(0, "value1")
        self.hashmap.put(8, "value2")
        self.assertEqual(self.hashmap.get(0), "value1")
        self.assertEqual(self.hashmap.get(8), "value2")
        #Tests to see if they are in the same bucket
        self.hashmap.put(1, "value3")
        self.hashmap.put(9, "value4")
        bucket0 = self.hashmap._buckets[0]
        bucket1 = self.hashmap._buckets[1]
        self.assertEqual(len(bucket0), 2)
        self.assertEqual(len(bucket1), 2)

class TestListMapping(unittest.TestCase):
    """Class which holds all testcases for the ListMapping class, used within Hashmap. MP"""
    def setUp(self):
        """Holds a ListMapping object to be used in each test. MP"""
        self.mapping = ListMapping()

    def test_init(self):
        """Testcase to handle correct initialization of a ListMapping object. MP"""
        self.assertEqual(len(self.mapping._entries), 0)

    def test_put(self):
        """Testcase to handle putting a new key-value pair into ListMapping. MP"""
        self.mapping.put("CSE1010", "Introduction to Python") 
        self.assertEqual(self.mapping.get("CSE1010"), "Introduction to Python")
        self.assertEqual(len(self.mapping._entries), 1)
        #Tests duplicate entry being added.
        self.mapping.put("CSE1010", "Introduction to Python") 
        self.assertEqual(len(self.mapping._entries), 1)

    def test_get(self):
        """Testcase to handle retrieving a value for a given key. MP"""
        self.mapping.put("CSE2050", "Data Structures and Algorithms")
        value = self.mapping.get("CSE2050")
        self.assertEqual(value, "Data Structures and Algorithms")

    def test_contains_(self):
        """Testcase to check the dunder method contains has correct functionality. MP"""
        #Should return True
        self.mapping.put("CSE2301", "Logic Systems and Programming")
        self.assertTrue("CSE2301" in self.mapping) 
        #Should return False
        self.assertFalse("CSE2500" in self.mapping)

class TestEnrollment(unittest.TestCase):
    """Class which holds all testcases relevant to testing proper student enrollment behavior."""
    def setUp(self):
        """Objects to be used in testcases under class TestEnrollment. MP"""
        self.course1 = Course("CSE2050", 3, 30)
        self.course2 = Course("CSE1010", 3, 50)
        self.student1 = Student("STU00001", "Student_1")
        self.student2 = Student("STU00002", "Student_2")
        self.student3 = Student("STU00003", "Student_3")
        self.student4 = Student("STU00004", "Student_4")
        self.student5 = Student("STU00005", "Student_5")
        self.course1.prerequisite.put("CSE2050", ["CSE1010"])
        self.student1.enroll(self.course2, "A")
        self.student2.enroll(self.course2, "B")
        self.student3.enroll(self.course2, "A")
        self.student5.enroll(self.course2, "F")

    def test_request_enroll_(self):
        """Tests that a student is enrolled/waitlisted given they meet the requirements, otherwise should raise an exception. MP"""
        with self.assertRaises(ValueError):
            #student4 does not have the prerequisite to take CSE2050
            self.course1.request_enroll(self.student4, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(2026, 12, 1)) 
        self.course1.request_enroll(self.student2, date(2026, 12, 1)) 
        self.course1.request_enroll(self.student3, date(2026, 12, 1))
        #should have enrolled remaining students given they meet prerequisites
        self.assertEqual(len(self.course1.enrolled_roster), 3)
        #trying to enroll failing student
        with self.assertRaises(ValueError):
            self.course1.request_enroll(self.student5, date(2026, 12, 1))

class TestSortingAlgorithms(unittest.TestCase):
    """Class which holds all testcases for the Merge sort and Quick sort algorithms implemented for Milestone 3. MP"""
    def setUp(self):
        """Holds course and student objects to be used in later testcases. Reused code from 
        unittests from MileStone 2 for sorting algorithms. MA, MP"""
        self.course1 = Course("CSE2050", 3, 30)
        self.student1 = Student("STU00001", "Student_1")
        self.student2 = Student("STU00002", "Student_2")
        self.student3 = Student("STU00003", "Student_3")
        self.student4 = Student("STU00004", "Student_4")
        self.student5 = Student("STU00005", "Student_5")
        self.student6 = Student("STU00006", "Student_6")
        
        self.course1.request_enroll(self.student6, date(2026, 12, 1))
        self.course1.request_enroll(self.student1, date(1950, 11, 1))
        self.course1.request_enroll(self.student3, date(2026, 9, 1))
        self.course1.request_enroll(self.student2, date(2001, 7, 21))
        self.course1.request_enroll(self.student4, date(2026, 9, 3))
        self.course1.request_enroll(self.student5, date(2026, 9, 5))
    
    def test_merge_sort_student_id(self):
        """Testcase to ensure correct order of students are returned upon merge sorting by id. MP"""
        test_sorted_list = ["STU00001", "STU00002", "STU00003", "STU00004", "STU00005", "STU00006"] 
        self.course1.sort_enrolled("id", "merge")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.student_id, test_sorted_list[i])
    
    def test_merge_sort_name(self):
        """Testcase to ensure correct order of students are returned upon merge sorting by name. MP"""
        test_sorted_list = ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6"] 
        self.course1.sort_enrolled("name", "merge")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.name, test_sorted_list[i])
    
    def test_merge_sort_date(self):
        """Testcase to ensure correct order of students are returned upon merge sorting by date. MP"""
        test_sorted_list = [date(1950, 11, 1), date(2001, 7, 21), date(2026, 9, 1), date(2026, 9, 3), date(2026, 9, 5), date(2026, 12, 1)]
        self.course1.sort_enrolled("date", "merge")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].enroll_date, test_sorted_list[i])  

    def test_quick_sort_student_id(self):
        """Testcase to ensure correct order of students are returned upon quick sorting by id. MP"""
        test_sorted_list = ["STU00001", "STU00002", "STU00003", "STU00004", "STU00005", "STU00006"] 
        self.course1.sort_enrolled("id", "quick")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.student_id, test_sorted_list[i])

    def test_quick_sort_name(self):
        """Testcase to ensure correct order of students are returned upon quick sorting by name. MP"""
        test_sorted_list = ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6"] 
        self.course1.sort_enrolled("name", "quick")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].student.name, test_sorted_list[i]) 

    def test_quick_sort_date(self):
        """Testcase to ensure correct order of students are returned upon quick sorting by date. MP"""
        test_sorted_list = [date(1950, 11, 1), date(2001, 7, 21), date(2026, 9, 1), date(2026, 9, 3), date(2026, 9, 5), date(2026, 12, 1)]
        self.course1.sort_enrolled("date", "quick")
        for i in range(len(test_sorted_list)):
            self.assertEqual(self.course1.enrolled_roster[i].enroll_date, test_sorted_list[i])

unittest.main()