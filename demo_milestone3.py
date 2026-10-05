import husky as h
import csv

#Milestone 3 - Reading in csv file data alongside other demonstrations.
#Milestone 1 demo found in main husky.py file, demos for Milestone 2 and 3 are in this file.
#Implemented by Michelle P and Michael A.

#course catalog CSE10
UConn = h.University()  #central manager, University object UConn

course_catalog = "course_catalog_CSE10_with_capacity.csv" 
cc_fields = []
cc_rows = []
with open(course_catalog, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    cc_fields = next(csvreader)
    for row in csvreader:
        cc_rows.append(row)
        course_id = row[0]
        course_title = row[1]  #not used
        credits = int(row[2])
        department = row[3]   #not used
        capacity = int(row[4])

        UConn.add_course(course_id, credits, capacity)

#university data
university_data = "university_data.csv"
ud_fields  = []
ud_rows = []
print(f"List of all enrollments and additions to waitlist:")
    
with open(university_data, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    ud_fields = next(csvreader)
    for row in csvreader:
        ud_rows.append(row)
        student_id = row[0]
        name = row[1]
        courses_string = row[2]
        UConn.add_student(student_id, name)

#enrollments CSE10

enrollments = "enrollments_CSE10.csv" 
e_fields = []
e_rows = []
with open(enrollments, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    e_fields = next(csvreader)
    for row in csvreader:
        e_rows.append(row)
        student_id = row[0]
        course_id = row[1]
        term = row[2]         #not used
        grade = row[3]
        attempt = int(row[4]) #not used

        #Demonstration 1/2: Shows all enrollments in courses and all reaching capacity.
        (UConn.get_course(course_id).request_enroll(UConn.get_student(student_id)))
        

#cse prerequisites, MP
prereqs = "cse_prerequisites.csv"
pr_fields = []
pr_rows = []
with open(prereqs, 'r') as csvfile:  #might need tab delimiter.. /t
    csvreader = csv.reader(csvfile)
    pr_fields = next(csvreader)
    for row in csvreader:
        if len(row) >= 1:
            course_code = row[0].strip()
            prerequisite = row[1].strip() if len(row) > 1 and row[1].strip() else None

            if course_code in UConn.courses and prerequisite:
                course = UConn.courses[course_code]
                try: 
                    current = course.prerequisite.get(course_code)
                    if prerequisite not in current:
                        current.append(prerequisite)
                        course.prerequisite.put(course_code, current)
                except KeyError:
                    #no prereqs yet
                    course.prerequisite.put(course_code, [prerequisite])


#Demonstration 3: Shows students being sorted by ID, and prints sorted enrolled_roster attribute of Course
UConn.get_course("CSE3500").sort_enrolled("date","bubble")

#Demonstration 4/5: Dropping a student from a given course. Showing that the next waitlisted student is enrolled.
print(UConn.get_course("CSE3500").drop("STU00179"))
print(UConn.get_course("CSE3500").enrolled_roster)    #can no longer find Student_179 in enrolled_roster



