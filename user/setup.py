from typing import Type, TypeVar, Optional
from user import models
from datetime import datetime


def get_largest_custom_id(_type: str = "student", **kwargs) -> int:
  sep: str = kwargs.get("seperator", " ")
  id: int = kwargs.get("max_id", None)
  if id:
    return id + 1
  
  model = models.Student if _type == "student" else models.Staff
  
  instances = model.objects.all()
  if not instances:
    return 0
  
  instance_id_list = []
  if _type == "student":
    instance_id_list = [int(x.student_id.split(sep)[1]) for x in instances]
  elif _type == "staff":
    instance_id_list = [int(x.staff_id.split(sep)[1]) for x in instances]
    
  if len(instance_id_list) == 0:
    return 0
    
  max_id  = max(instance_id_list)
  return max_id


def generate_custom_id(_type: str = "student", prefix: str = "STU", length: int = 5, seperator: str = " ") -> Optional[str]:
  try:    
    id = get_largest_custom_id(_type) + 1
    str_id = str(id).zfill(length)
    new_id = f"{prefix}{seperator}{str_id}"

    existing_instance_with_new_id = None
    if _type == "student":
      existing_instance_with_new_id = models.Student.objects.filter(student_id=new_id)
    elif _type == "staff":
      existing_instance_with_new_id = models.Staff.objects.filter(staff_id=new_id)
      
    if not existing_instance_with_new_id:
      return new_id
  except Exception as e:
    print(f"Exception while generating instance id: {e}")
    return None


def get_largest_student_id(**kwargs) -> int:
  sep: str = kwargs.get("seperator", " ")
  id: int = kwargs.get("max_id", None)
  if id:
    return id + 1
  
  students = models.Student.objects.all()
  if not students:
    return 0

  try:
    student_id_list = [int(x.student_id.split(sep)[1]) for x in students]
    max_id  = max(student_id_list)
  except Exception as e:
    return len(students)

  return max_id


def generate_student_id(prefix: str = "STU", length: int = 5, seperator: str = " ") -> Optional[str]:
  try:
    id = get_largest_student_id() + 1
    str_id = str(id).zfill(length)
    new_id = f"{prefix}{seperator}{str_id}"
    
    existing_student_with_new_id = models.Student.objects.filter(student_id=new_id)
    if not existing_student_with_new_id:
      return new_id
  except Exception as e:
    print(f"Exception while generating student id: {e}")
    return None


def get_largest_student_matric(template: str, **kwargs) -> int:
  pass


def generate_student_matric(student: models.Student, length: int = 3, seperator: str = "") -> Optional[str]:
  try:
    year = str(datetime.today().year)[-2:]
    specialization_code = str(student.specialization.code)[-2:]
    department_code = str(student.specialization.department.code)[-2:]
    faculty_code = str(student.specialization.department.faculty.code)[-2:]
    proto_matric_no = f"{year}{faculty_code}{department_code}{specialization_code}"
    
    students = models.Student.objects.filter(matric_no__icontains=proto_matric_no)
    max_matric = len(students)
    new_matric = max_matric + 1
    
    str_matric = str(new_matric).zfill(length)
    new_matric = f"{proto_matric_no}{str_matric}"
    
    existing_student_with_new_matric = models.Student.objects.filter(matric_no=new_matric)
    if not existing_student_with_new_matric:
      return new_matric
  except Exception as e:
    print(f"Exception while generating student id: {e}")
    return None


def get_largest_staff_id(**kwargs) -> int:
  sep: str = kwargs.get("seperator", " ")
  id: int = kwargs.get("max_id", None)
  if id:
    return id + 1
  
  staff = models.Staff.objects.all()
  if not staff:
    return 0
  
  try:
    staff_id_list = [int(x.staff_id.split(sep)[1]) for x in staff]
    max_id  = max(staff_id_list)
  except Exception as e:
    return len(staff)

  return max_id


def generate_staff_id(prefix: str = "EMP", length: int = 5, seperator: str = " ") -> Optional[str]:
  try:
    id = get_largest_staff_id() + 1
    str_id = str(id).zfill(length)
    new_id = f"{prefix}{seperator}{str_id}"
    
    existing_staff_with_new_id = models.Staff.objects.filter(employee_id=new_id)
    if not existing_staff_with_new_id:
      return new_id
  except Exception as e:
    print(f"Exception while generating staff id: {e}")
    return None
