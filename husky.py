import csv
from datetime import date
#Milestone 1&2&3 by Michelle P (MP) and Mike A (MA).
#MP and MA refer to the person(s) responsible for that section.
#Note that we also added additional __repr__ methods per class for Milestone 2 to make debugging easier.

class Course:
    """Defines the Course class which is intended to deal with methods and data regarding 
    student courses. MP, MA"""
    def __init__(self, course_code, credits, capacity=0, students=None): 
        """Defines attributes course_code, credits and initializes 
        an empty list for the student roster. MP, MA"""
        if students is None:
            students = []
        self.course_code = course_code
        self.credits = credits
        self.students = students
        self.capacity = capacity
        self.waitlist = LinkedQueue()
        self.enrolled_roster = []
        self.enrolled_sorted_by = ""
        self.prerequisite = HashMap()

    def add_student(self, student):
        """Adds a student to the class roster, prevents duplicate objects from being added. MP, MA"""
        if student in self.students:
            raise NameError("Student already enrolled in course.")
        else:
            self.students.append(student)

    def get_student_count(self):
        """Returns the amount of students enrolled in the class. MP, MA"""
        return len(self.students)
    
    def request_enroll(self, student, enroll_date=None):
        """Enrolls given student in Course if capacity is not full, otherwise adds
        student to waitlist. MA,MP"""
        #get prereqs first
        try:
            required_prereqs = self.prerequisite.get(self.course_code)
        except:
            required_prereqs = []
        #check if student is missing prereqs, then don't allow enrollment
        missing_prereqs = []
        for prereq in required_prereqs:
            has_completed = False 
            for course in student.courses:
                if course.course_code == prereq:
                    #check that student passed the course
                    grade = student.courses[course]
                    if grade != 'F':
                        has_completed = True
                    break 
        
            if not has_completed:
                missing_prereqs.append(prereq)
        #if missing prereqs, raise an exception
        if missing_prereqs:
            raise ValueError("Student is missing prerequisites to enroll in requested course.")
        for record in self.enrolled_roster:
            #raises a ValueError if student is found is be enrolled in course, comparison via ID.
            if record.student.student_id == student.student_id:
                raise ValueError("Student already enrolled in course.")
        if len(self.enrolled_roster) < self.capacity:
                #Enrolls the student if there is enough space.
            self.enrolled_roster.append(EnrollmentRecord(student, enroll_date))
            return f"Enrolled {student.name} in {self.course_code}"
        else:
                #Adds student to waitlist if capacity full.
            self.waitlist.enqueue(student)
            return f"{student.name} added to waitlist for {self.course_code}. Capacity full."
        
    def drop(self, student_id, enroll_date_for_replacement=None):
        """Drops given student by their ID, and if waitlist is not empty dequeues student on
        the waitlist to be added to the same course. Needs to check if a given list is sorted 
        because binary search is used. Updates enroll_date_for_replacement. MA,MP"""
        dropped_record = self.enrolled_roster.pop(recursive_binary_search(self.enrolled_roster, student_id, 0, len(self.enrolled_roster)))
        if self.waitlist.is_empty() == False:
            applicant = self.waitlist.dequeue()
            self.enrolled_roster.append(EnrollmentRecord(applicant, enroll_date_for_replacement))
            return f"{dropped_record.student.name} has been dropped from {self.course_code} and {applicant.name} has been added to {self.course_code}."
        else:
            return f"{dropped_record.student.name} has been dropped from {self.course_code}."

    def sort_enrolled(self, by, algorithm):
        """Sorts the list enrolled roster by name, id, or date using a sorting agorithm currently either bubble sort or insertion sort. MA,MP"""
        if by not in ["name","id","date"]:
            raise ValueError("Input: name, id, or date")
        elif algorithm not in ["bubble", "insertion", "merge", "quick"]:
            raise ValueError("Input: bubble or insertion")
        else:
            R = self.enrolled_roster
            if by == "name":
                self.enrolled_sorted_by = "name"
                if algorithm == "bubble":
                    return bubble_sort_name(R)
                elif algorithm == "insertion":
                    return insertion_sort_name(R)
                elif algorithm == "merge":
                    return merge_sort_name(R)
                elif algorithm == "quick":
                    return quick_sort_name(R)
            elif by == "id":
                self.enrolled_sorted_by = "id"
                if algorithm == "bubble":
                    return bubble_sort_student_id(R)
                elif algorithm == "insertion":
                    return insertion_sort_student_id(R)
                elif algorithm == "merge":
                    return merge_sort_student_id(R)
                elif algorithm == "quick":
                    return quick_sort_student_id(R)
            elif by == "date":
                self.enrolled_sorted_by = "date"
                if algorithm == "bubble":
                    return bubble_sort_date(R)
                elif algorithm == "insertion":
                    return insertion_sort_date(R)
                elif algorithm == "merge":
                    return merge_sort_date(R)
                elif algorithm == "quick":
                    return quick_sort_date(R)
    
    def __repr__(self):
        """Dunder method to change string representation of Course object when printing to terminal. MP"""
        return f"Course({self.course_code}, {self.credits}, {self.capacity}, {self.students})"

class Student():
    """Defines the Student class which deals with methods regarding individual students. MA,MP"""
    GRADE_POINTS = {
        'A' : 4.0, 'A-' : 3.7,
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
        'D' : 1.0,
        'F' : 0.0
        }
    
    def __init__(self, student_id, name, courses=None):
        """Defines attributes student_id, name, courses. MP"""
        if courses is None:
            courses = {}
        self.student_id = student_id    
        self.name = name
        self.courses = courses

    def __repr__(self):
        """Dunder method to change string representation of Student object when printing to terminal. MP"""
        return f"Student({self.student_id}, {self.name}, {self.courses})"

    def enroll(self, course, grade):
        """Enrolls a student in course using corse object and grade as inputs. MA"""
        if grade not in Student.GRADE_POINTS:
            raise KeyError("Grade entered is not a valid letter grade.MA,MP")
        else:
            self.courses[course] = grade
            course.add_student(self)

    def update_grade(self, course, grade):
        """Updates the grade of a course for a student using corse object and grade as inputs. MA"""
        if grade not in Student.GRADE_POINTS:
            raise KeyError("Grade entered is not a valid letter grade.")
        else:
            self.courses[course] = grade

    def calculate_gpa(self):
        """Calculates the GPA of the student taking into account total credits and course grades.
        Returns 0.00 for GPA if no credits have been earned. MA, MP"""
        total_credits = 0
        total_points = 0
        
        for course, grade in self.courses.items():
            if grade not in Student.GRADE_POINTS:
                raise KeyError("Grade entered is not a valid letter grade.")
            elif grade in Student.GRADE_POINTS:
                total_points += Student.GRADE_POINTS[grade] * course.credits
                total_credits += course.credits

        if total_credits == 0:
            return 0.00
        else:
            GPA = total_points / total_credits
            return round(GPA, 2)
            
    def get_courses(self):
        """Returns a list which the names of all courses (keys) a student is taking. MP"""
        course_list = []
        for course in self.courses:
            course_list.append(course.course_code)
        return course_list

    def get_course_info(self):
        """Gets a list of a student's courses grades and credits. MA"""
        info = []
        for course in self.courses:
            info.append(f"{course.course_code}: Grade {self.courses[course]}, Credits {course.credits}")
        return info
    
class University:
    """Defines the University class, the central manager. MA"""
    def __init__(self, students=None, courses=None):
        """Defines attributes students and courses, which are both dictionaries which
        store Student and Course objects mapped to respective student IDs and course codes. MP"""
        if students is None:
            students = {}
        if courses is None:
            courses = {}
        self.students = students
        self.courses = courses

    def add_course(self,course_code, credits, capacity=0):
        """Adds a course object to the University class. MA"""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits, capacity)
        else:
            raise KeyError("Course already added.")
        return self.courses[course_code]

    def add_student(self,student_id, name):
        """Adds a student object to the University class. MA"""
        if len(student_id) != 8:
            raise ValueError("Student ID needs to be eight characters long.")
        if student_id[0:3] != "STU":
            raise KeyError("Student ID needs to begin with STU.")
        if student_id in self.students:
            raise KeyError("Student ID already in use.")
        
        student = Student(student_id, name)
        self.students[student_id] = student
        return self.students[student_id]

    def get_student(self,student_id):
        """Gets a student object from the University class matching given student ID. MA"""
        if len(student_id) != 8:
            raise ValueError("Student ID needs to be eight characters long.")  
        if student_id[0:3] != "STU":
            raise KeyError("Student ID needs to begin with STU.")
        return self.students.get(student_id)

    def get_course(self,course_code):
        """Gets a course object from the University class. MA"""
        if course_code in self.courses:
            return self.courses.get(course_code)
        else:
            raise KeyError("Course does not exist.")

    def get_course_enrollment(self,course_code):
        """Gets the amount of students enrolled in a course. MA"""
        if course_code in self.courses:
            course = self.get_course(course_code)
            return course.get_student_count()
        else:
            raise KeyError("Course does not exist.")

    def get_students_in_course(self,course_code):
        """Gets a list of students enrolled in a course. MA"""
        if course_code in self.courses.keys():
            students_list = []
            for i in self.students:
                if course_code in self.students[i].get_courses():
                    students_list.append(self.students[i].student_id)
            return students_list
        else:
            raise KeyError("Course does not exist.") 
    
    def __repr__(self):
        """Dunder method to change string representation of University object when printing to terminal. MP"""
        return f"University({self.students}, {self.courses})"

#Milestone 2

class EnrollmentRecord:
    """Class to represent enrollment in a specific course, with student object and enroll_date. MA,MP"""
    def __init__(self, student, enroll_date=None):
        """Defines attributes student and enroll_date. Makes sure to validate the string and
        convert or raise an error if necessary. Referenced GeeksForGeeks datetime module tutorial and explanation of the datetime module. MA,MP"""
        self.student = student
        if enroll_date == None:
            self.enroll_date = date.today()
        elif isinstance(enroll_date, str):
            try:
                self.enroll_date = date.fromisoformat(enroll_date)
            except ValueError:
                raise ValueError(f"Incorrect date format {enroll_date}. Must be YYYY-MM-DD.")
        elif isinstance(enroll_date, date):
            self.enroll_date = enroll_date
        else:
            raise ValueError(f"Enroll_date attribute must be None, string, or date attribute. Instead was {type(enroll_date)}.")

    def __repr__(self):
        """Dunder method to change string representation of EnrollmentRecord object when printing to console. MP"""
        return f"Enrollment Record({self.student}, {self.enroll_date})"

class Node:
    """Class for Node objects to be stored inside of LinkedQueue. MA"""
    def __init__(self, data, next=None):
        """Defines data and next attributes for Node objects. MA"""
        self.data = data
        self.next = next

class LinkedQueue: 
    """Main ADT to handle waitlist behavior. Utilized external resource GeeksForGeeks, detailing
    how to create a LinkedQueue without the use of a python list. MA,MP"""
    def __init__(self):
        """Defines private attributes _head, _tail, and _size for LinkedQueue. MA"""
        self.head = None
        self.tail = None
        self.size = 0
    
    def enqueue(self, item):
        """Adds a new node to the end of the LinkedQueue. MA,MP"""
        new_node = Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
            self.size += 1
        else:
            self.tail.next = new_node
            self.tail = new_node  
            self.size += 1 
        
    def dequeue(self):
        """Dequeues an element from the beginning of LinkedQueue (FIFO). MA,MP"""
        if self.is_empty():
            raise ValueError("Queue is empty.")
        item = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return item
        
    def is_empty(self):
        """Checks if LinkedQueue is empty, returns True/False. MA"""
        return self.size == 0

    def __len__(self):
        """Dunder method to return length of LinkedQueue list. MP"""
        return self.size
    
def recursive_binary_search(records, target_id, low, high, is_sorted = False):
    """Uses recursion to search for target student by ID. Uses is_sorted to 
    check if records is already sorted for binary search operation. MA,MP"""  
    if is_sorted == False:     #handles option A for Task 5
        bubble_sort_student_id(records)
    if low > high:   
        return -1
    mid = low + (high - low) // 2     
    current_id = records[mid].student.student_id
    if current_id == target_id:
        return mid 
    elif records[mid].student.student_id > target_id:
        return recursive_binary_search(records, target_id, low, mid-1, True)
    else:
        return recursive_binary_search(records, target_id, mid+1, high, True)
        

def bubble_sort_student_id(records):
    """Bubble sort algorithm, takes a list of IDs from EnrollmentRecord objects. 
    Used lecture code from Mod7 as reference. MA,MP"""
    n = len(records)
    for i in range(n):
        swapped = False   #if the list is already sorted, break
        for j in range(0, n-i-1):
            if records[j].student.student_id > records[j+1].student.student_id:
                records[j], records[j+1] = records[j+1], records[j] 
                swapped = True
        if swapped == False:
            break

def bubble_sort_name(records):
    """Bubble sort algorithm, takes a list of names from EnrollmentRecord objects.
    Used lecture code from Mod7 as reference. MA,MP"""
    n = len(records)
    for i in range(n):
        swapped = False   #if the list is already sorted, break
        for j in range(0, n-i-1):
            if records[j].student.name > records[j+1].student.name:
                records[j], records[j+1] = records[j+1], records[j] 
                swapped = True
        if swapped == False:
            break

def bubble_sort_date(records):
    """Bubble sort algorithm, takes a list of enroll+dates from EnrollmentRecord objects. 
    Referenced lecture code from Mode7. MA,MP"""
    n = len(records)
    for i in range(n):
        swapped = False   #if the list is already sorted, break
        for j in range(0, n-i-1):
            if records[j].enroll_date > records[j+1].enroll_date:
                records[j], records[j+1] = records[j+1], records[j] 
                swapped = True
        if swapped == False:
            break

def insertion_sort_student_id(records):
    """Insertion sort algorithm, takes a list of IDs from EnrollmentRecord objects. 
    Used lecture code from Mod7 as reference. MA,MP"""
    for i in range(1, len(records)):
        key_record = records[i]  #object EnrollmentRecord
        key_ID =  records[i].student.student_id  #attribute student_id inside of object
        j = i - 1
        while j >= 0 and key_ID < records[j].student.student_id:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = key_record

def insertion_sort_name(records):
    """Insertion sort algorithm, takes a list of names from EnrollmentRecord objects.
    Used lecture code from Mod7 as reference. MA,MP"""
    for i in range(1, len(records)):
        key_record = records[i]  #object EnrollmentRecord
        key_name =  records[i].student.name 
        j = i - 1
        while j >= 0 and key_name < records[j].student.name:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = key_record

def insertion_sort_date(records):
    """Insertion sort algorithm, takes a list of enroll_dates from EnrollmentRecord objects.
    Used lecture code from Mod7 as reference. MA,MP"""
    for i in range(1, len(records)):
        key_record = records[i]  #object EnrollmentRecord
        key_name =  records[i].enroll_date  
        j = i - 1
        while j >= 0 and key_name < records[j].enroll_date:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = key_record

def _merge_student_id(A,B,L):
    """Private method to be used inside of the merge_sort_student_id algorithm. MA, MP""" 
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i].student.student_id < B[j].student.student_id:
            L[i+j] = A[i]
            i += 1
        else:
            L[i+j] = B[j]
            j += 1
    L[i+j:] = A[i:] + B[j:]

def _merge_name(A,B,L):
    """Private method to be used inside of the merge_sort_name algorithm. MA, MP"""
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i].student.name < B[j].student.name:
            L[i+j] = A[i]
            i += 1
        else:
            L[i+j] = B[j]
            j += 1
    L[i+j:] = A[i:] + B[j:]

def _merge_date(A,B,L):
    """Private method to be used inside of the merge_sort_date algorithm. MA, MP"""
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i].enroll_date < B[j].enroll_date:
            L[i+j] = A[i]
            i += 1
        else:
            L[i+j] = B[j]
            j += 1
    L[i+j:] = A[i:] + B[j:]

def _partition_student_id(L,low,high):
    """Private partition method to be used inside of the quick_sort_student_id algorithm. MA, MP"""
    pivot = L[high].student.student_id
    i = low
    
    for j in range(low, high):
        if L[j].student.student_id <= pivot:
            L[i], L[j] = L[j], L[i]
            i += 1
    
    L[i], L[high] = L[high], L[i]
    return i

def _partition_name(L,low,high):
    """Private partition method to be used inside of the quick_sort_name algorithm. MA, MP"""
    pivot = L[high].student.name
    i = low
    
    for j in range(low, high):
        if L[j].student.name <= pivot:
            L[i], L[j] = L[j], L[i]
            i += 1
    
    L[i], L[high] = L[high], L[i]
    return i

def _partition_date(L,low,high):
    """Privae partition method to be used inside of the quick_sort_date algorithm. MAMA, MP"""
    pivot = L[high].enroll_date
    i = low
    
    for j in range(low, high):
        if L[j].enroll_date <= pivot:
            L[i], L[j] = L[j], L[i]
            i += 1
    
    L[i], L[high] = L[high], L[i]
    return i

def merge_sort_student_id(L):
    """Merge sort algorithm which uses student_id as the key to sort. MA"""
    if len(L) == 1:
        return L
    mid = len(L)//2
    A = L[:mid]
    B = L[mid:] 
    merge_sort_student_id(A)
    merge_sort_student_id(B)
    _merge_student_id(A,B,L)
    return L

def merge_sort_name(L):
    """Merge sort algorithm which uses the name of each student as the key to sort. MA"""
    if len(L) == 1:
        return L
    mid = len(L)//2
    A = L[:mid]
    B = L[mid:] 
    merge_sort_name(A)
    merge_sort_name(B)
    _merge_name(A,B,L)
    return L 

def merge_sort_date(L):
    """Merge sort algorithm which uses the date as the key to sort. MA"""
    if len(L) == 1:
        return L
    mid = len(L)//2
    A = L[:mid]
    B = L[mid:] 
    merge_sort_date(A)
    merge_sort_date(B)
    _merge_date(A,B,L)
    return L 

def quick_sort_student_id(L, left=0, right=None):
    """Quick sort algorithm which uses the student_id as the key to sort. MAQuick sort algorithm which uses the id of each student as the key to sort. MA"""
    if right is None:
        right = len(L) - 1
    if right - left <= 1:
        return L
    pivot = _partition_student_id(L, left, right) 
    quick_sort_student_id(L, left, pivot - 1)
    quick_sort_student_id(L, pivot + 1, right)
    return L

def quick_sort_name(L, left=0, right=None):
    """Quick sort algorithm which uses the name as the key to sort. MAQuick sort algorithm which uses the name of each student as the key to sort. MA"""
    if right is None:
        right = len(L) - 1
    if right - left <= 1:
        return L
    pivot = _partition_name(L, left, right) 
    quick_sort_name(L, left, pivot - 1)
    quick_sort_name(L, pivot + 1, right)
    return L

def quick_sort_date(L, left=0, right=None):
    """Quick sort algorithm which uses the date as the key to sort. MAQuick sort algorithm which uses the date of each student's enrollment as 
    the key to sort. MA"""
    if right is None:
        right = len(L) - 1
    if right - left <= 1:
        return L
    pivot = _partition_date(L, left, right) 
    quick_sort_date(L, left, pivot - 1)
    quick_sort_date(L, pivot + 1, right)
    return L

class Entry:
    """Class to initialize individual entry objects to be stored inside of the ListMapping ADT.
    Used Mod 8 Lecture code as reference."""
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + " : " + str(self.value)
    
class ListMapping: 
    """Class to create the ListMapping ADT to be used in the HashMapping class.
    Used Mod 8 Lecture code as reference. MP, MA"""
    def __init__(self):
        self._entries = []

    def __len__(self):
        """Returns the number of entries inside the list. MP"""
        return len(self._entries)

    def put(self, key, value):
        """Adds an entry if the given key is not in _entries, otherwise updates the value at the 
        given key. MP"""
        e = self._entry(key)
        if e is not None:
            e.value = value 
        else: 
            self._entries.append(Entry(key, value))

    def get(self, key): 
        """Returns the value of the entry at the given key, otherwise raises a KeyError. MP"""
        e = self._entry(key)
        if e is not None:
            return e.value 
        else:
            raise KeyError(f"Key not found.")

    def _entry(self, key):
        """Private method used to return an entry in the ListMap given a key. If not found
        returns None. MP"""
        for e in self._entries:
            if e.key == key:
                return e 
        return None
    
    def __contains__(self, key):
        """Dunder method which allows "in" to check if key exists. MP"""
        return self._entry(key) is not None
    
    def __setitem__(self, key, value):
        """Dunder method which allows you to use bracket notation to set new values. MP"""
        self.put(key, value)
    
    def __getitem__(self, key):
        """Dunder method which allows you to use bracket notation to return items using key. MP"""
        return self.get(key)

    def items(self):
        """Returns an iterator that iterates over the values in the mapping. MA"""
        return ((e.key, e.value) for e in self._entries)
    
    def values(self):
        """Returns an iterator that iterates over the key-value pairs in the mapping. MA"""
        return (e.value for e in self._entries)

class HashMap:
    """A mapping using a hashtable and rehashing to handle hash collisions when necessary. 
    Used Mod 8 Lecture code as reference. MP, MA"""
    def __init__(self, size=2):
        """Defines private attributes _size, _buckts, and _length for HashMap. MA"""
        self._size = size
        self._buckets = [ListMapping() for _ in range(self._size)]
        self._length = 0
        
    def __len__(self):
        """Dunder methodd to return the number of items in the HashMap. MP"""
        return self._length

    def _bucket(self, key):
        """Finds the correct bucket for the given key. MA"""
        return self._buckets[hash(key) % self._size]
    
    def put(self, key, value):
        """Puts in a new key-value pair into the hashmap, triggers rehash if reaches 0.8 load factor. MP"""
        bucket = self._bucket(key)
        if key not in bucket:
            self._length += 1
            bucket.put(key, value)
        else:
            bucket.put(key, value)
        if self._length / self._size >= 0.8:
            self._rehash()

    def get(self, key):
        """Retrieves the value for a given key. MP"""
        bucket = self._bucket(key)
        return bucket.get(key)
    
    def _rehash(self):
        """Doubles the size of the number of buckets and rehashes the HashMap. MA"""
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [ListMapping() for _ in range(self._size)]
        self._length = 0
        for bucket in old_buckets:
            for key, value in bucket.items():
                self.put(key, value)
    
    def __setitem__(self, key, value):
        """Dunder methodd to set a key value pair as if it where a dictionary and increases the length value. MA"""
        self.put(key, value)

    def __getitem__(self, key):
        """Dunder method to get a value by useing the form self[key]. MA"""
        m = self._bucket(key)
        return m[key]

if __name__ == "__main__":
    #Loading all data from csv files, MP, MA
    UConn = University()
    
    course_catalog = "course_catalog.csv" 
    cc_fields = []
    cc_rows = []
    with open(course_catalog, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        cc_fields = next(csvreader)
        for row in csvreader:
            cc_rows.append(row)
            course_code = row[0]
            credits = int(row[1])
            UConn.add_course(course_code, credits)


    university_data = "university_data.csv"
    ud_fields  = []
    ud_rows = []
    
    with open(university_data, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        ud_fields = next(csvreader)
        for row in csvreader:
            ud_rows.append(row)
            student_id = row[0]
            name = row[1]
            courses_string = row[2]
            temp_courses_and_grade = courses_string.split(";")
            courses = {}
            UConn.add_student(student_id, name)
            for i in temp_courses_and_grade:
                temp_courses = i.split(":")
                temp_course_code = temp_courses[0]
                temp_grade = temp_courses[1]
                UConn.get_student(student_id).enroll(UConn.get_course(temp_course_code), temp_grade)

    #Demonstration section
    # Demo 1- Prints all students taking a specific course, such as "CSE3100". MP, MA      
    print(f"All students in CSE3100:\n{UConn.get_students_in_course("CSE3100")} \n")
    
    # Demo 2- Prints the GPA for a specific student, in this case Student_47. MP, MA
    print(f"GPA for Student 47: {UConn.get_student("STU00047").calculate_gpa()} \n")
    
    # Demo 3 - Prints all of the courses and course info (includes grades and credits)
    # for a specific student. MP, MA
    print(f"Courses and course info for Student 82: \n{UConn.get_student("STU00082").get_course_info()}\n")
    
    # Demo 4 - Calculates mean, mode and median for a course, in this case "CSE3100". MA
    # Prints all expected values below. MA
    list_of_students = UConn.get_students_in_course("CSE3100")
    list_of_grades = []
    t_grade = 0
    for i in list_of_students:
        for course, grade in UConn.get_student(i).courses.items():
            t_grade = Student.GRADE_POINTS[grade]
            list_of_grades.append(t_grade)

    #Mean:
    total = 0
    x = 0
    for i in list_of_grades:
        total += i
        x += 1
    mean = round(total/x, 2)

    # Mode:
    counts = {}
    for i in list_of_grades:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    max_count = 0
    for i in counts.values():
        if i > max_count:
            max_count = i
    for val, key in counts.items():
        if key == max_count:
            mode = val

    # Median:
    sorted_grades = sorted(list_of_grades)
    n = len(sorted_grades)
    if n % 2 == 1:
        mid = n // 2
        median = sorted_grades[mid]
    else:
        mid_1 = (n // 2) - 1
        mid_2 = n // 2
        median = (sorted_grades[mid_1] + sorted_grades[mid_2] / 2)
        median = round(median, 2)


    print(f"GPA of all students in the course CSE3100\nMean: {mean}\nMode: {mode}\nMedian: {median}\n")

    # Demo 5 - Calculates mean and median for the GPA of all students in the university. MA
    GPA_list = []
    for _, student in UConn.students.items():
        x = student.calculate_gpa()
        GPA_list.append(x)

    # Mean:
    total = 0
    x = 0
    for i in GPA_list:
        total += i
        x += 1
    mean_u = round(total/x, 2)

    #Median:
    sorted_grades = sorted(GPA_list)
    n = len(sorted_grades)
    if n % 2 == 1:
        mid = n // 2
        median_u = sorted_grades[mid]
    else:
        mid_1 = (n // 2) - 1
        mid_2 = n // 2
        median_u = (sorted_grades[mid_1] + sorted_grades[mid_2] / 2)
        median_u = round(median_u, 2)

    print(f"GPA of all students in the university UConn\nMean: {mean_u}\nMedian: {median_u}\n")

    # Demo 6 - Prints common students in two different courses (Intersection). 
    # Takes CSE1010 and PHYS1010 as examples. MP
    listCSE = UConn.get_students_in_course("CSE1010")
    listPHYS = UConn.get_students_in_course("PHYS1010")
    intersection_courses = set(listCSE) & set(listPHYS)
    common_courses = list(intersection_courses)
    print(f"List of all students which are taking CSE1010 and PHYS1010: \n{common_courses}\n")