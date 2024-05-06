from fastapi import FastAPI
import uvicorn
students =[{"student_id":1,"name":"talha","age":20,"class":"bscs"},{"student_id":2,"name":"asif","age":21,"class":"bsit"},
           {"student_id":3,"name":"mehmood","age":19,"class":"bsse"}]
app=FastAPI()
@app.get("/root")
def get_all_students():
    return "root"
@app.get("/students")
def get_all_students():
    return students
@app.get("/students/{student_id}")
def get_student(student_id:int):
    for student in students:
        if student["student_id"] == student_id:
            return student
    return "No record found"

@app.post("/students")
def add_student(name:str,age:int,add_class:str):
    global students
    students.append({"student_id":len(students)+1,"name":name,"age":age,"class":add_class})
    return "Student added"
@app.put("/students/{student_id}")
def update_student_recored(student_id:int,name:str,age:int,add_class:str):
    student_index=None
    for i,student in enumerate(students):
        if student["student_id"] ==student_id:
            student_index=i
            break
    if student_index is None:
        return "No student found"
    else:
        students[student_index]["name"] = name
        students[student_index]["age"] = age
        students[student_index]["class"] = add_class
        return f"record updated for {students[student_index]['name']}"
@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    student_index=None
    for i,student in enumerate(students):
        if student["student_id"]== student_id:
            student_index=i
            break
    if student_index is None:
         return "No record found"
    del students[student_index]
    return f"Deleted {students[student_index]['name']}"
def start():
    uvicorn.run("api.main:app",host="127.0.0.1",port=8080,reload=True)
start()