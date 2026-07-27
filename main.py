import json
from abc import ABC, abstractmethod
from pathlib import Path

database = "school_database.json"
data = {"students": [], "teachers": []}

if Path(database).exists():
    with open(database,'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)
            

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)
        


class Persons(ABC):
    
    @abstractmethod
    def get_roles(self):
        pass
    
    @abstractmethod
    def register(self):
        pass
    
    @abstractmethod
    def show_details(self):
        pass
    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email :
            return True
        else:
            return False

# Student regstration section
 
class Student(Persons):
    
    def get_roles(self):
        return "student"
    
    def register(self):
        name = input("Tell your name :-")
        age = int(input("Tell your age :-"))
        email = input("Tell your Email :-")
        roll_no = input("Tell your Roll number :-")
        
        if not Persons.validate_email(email):
            print("invalied Email")
            return
        
        for i in data ['students']:
            if i['roll_no'] == roll_no:
                print("Student already exists")
                return
            
        data['students'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "roll_no" : roll_no,
            "grades" : {},
        })
        save()
        print(f"Student {name} registered")
        
    def show_details(self):
        roll_no = input("roll no :-")
        for i in data['students']:
            if i['roll_no'] == roll_no:
                grades = i['grades']
                avg = sum(grades.values())/len(grades) if grades else 0
                
                print(f"\n Name : {s['name']}")
                print(f" Roll no : {s['roll_no']}")
                print(f" Grades : {grades}")
                print(f" Average : {avg:.1f}")
                return
    
    def add_grades(self):
        roll_no = input("Tell the roll number :-")
        subject = input("Subject :-") 
        marks = float(input("Marks :-"))
        
        for i in data['students']:
            if i["roll_no"] == roll_no:
                i['grades'] [subject] = marks
                save()
                print("Grade added successfully")
                return
        print("Student not found")
                
    
# Teacher regstration section
class Teacher(Persons):
    def get_roles(self):
        return "Teacher"
    
    def register(self):
        name = input("Tell your name :-")
        age = int(input("Tell your age :-"))
        email = input("Tell your Email :-")
        subject = input("subject :-")
        emp_id = input("Tell your emp_id number :-")
        
        if not Persons.validate_email(email):
                print("invalied Email")
                return
            
        for i in data ['teachers']:
            if i['emp_id'] == emp_id:
                print("Teacher already exists")
                return
        data['teachers'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "Subject" : subject,
            "emp_id" : emp_id,
        })
        save()
        print(f"Teacher {name} registered")
        
    def show_details(self):
        emp_id  = input("Employee ID:-")
        for i in data['teachers']:
            if i['emp_id'] == emp_id:
        
                print(f"\n Name : {i['name']}")
                print(f" Subject : {i['Subject']}")
                print(f" Employee ID : {i['emp_id']}")
                return
        print("Teacher not found.")

student = Student()
teacher = Teacher()

print("press 1 to register a student")
print("press 2 to register a Teacher")
print("press 3 to add grades")
print("press 4 to show students detail")
print("press 5 to show teacher detail")

choise = int(input("Please tell your choise :-"))

if choise == 1:
    student.register()
    
elif choise == 2:
    teacher.register()
    teacher.register()
    
    
elif choise == 3:
    student.add_grades()
    
elif choise == 4:
    student.show_details()
    
elif choise == 5:
    teacher.show_details()
