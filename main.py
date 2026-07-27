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
    def registermethod(self):
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
    
class Student(Persons):
    
    def get_roles(self):
        return "student"
    
    def registermethod(self):
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
        pass

student = Student()

print("press 1 to register a student")
print("press 2 to register a Teacher")
print("press 3 to add grades")
print("press 4 to show students detail")
print("press 5 to show teacher detail")

choise = int(input("Please tell your choise :-"))

if choise == 1:
    student.registermethod()
    
