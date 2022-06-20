
from typing import TypeVar, Type, Optional
from django.contrib.auth import get_user_model
from django.db.models import Model
from academics import models
from user import models as umodels

T = TypeVar('T', bound=Model)


def faculty_dean_helper(faculty: models.Faculty = None, dean :umodels.User = None, 
                        _pre: bool = False) -> Optional[umodels.User]:
  """Update faculty dean and update or create the staff instance for dean

  Args:
      faculty (models.Faculty, optional): The faculty to be updated. Defaults to None.
      dean (umodels.User, optional): The user to be set as dean. Defaults to None.
      _pre (bool, optional): Is the function called before model .save(). Defaults to False.

  Returns:
      Optional[umodels.User]: The dean user object
  """
  try:
    dean = dean if dean else faculty.dean
    if not dean.is_staff:
      raise Exception("Dean is not a staff")
    if not _pre:
      faculty.dean = dean
      faculty.save()
    
    defaults = {"is_dean_of_faculty": True}
    staff, created = umodels.Staff.objects.update_or_create(
      user=dean, specialization=dean.specialization, defaults=defaults)
    return dean
  except Exception as e:
    print("Exception geting dean:" if not created else "Exception updating dean staff model:", e)
    return None


def department_head_helper(department: models.Department = None, head :umodels.User = None, 
                           _pre: bool = False) -> Optional[umodels.User]:
  """Update department head and update or create the staff instance for head

  Args:
      department (models.Department, optional): The department to be updated. Defaults to None.
      head (umodels.User, optional): The user to be set as head. Defaults to None.
      _pre (bool, optional): Is the function called before model .save(). Defaults to False.

  Returns:
      Optional[umodels.User]: The head user object
  """
  try:
    head = head if head else department.head
    if not head.is_staff:
      raise Exception("Dean is not a staff")
    if not _pre:
      department.head = head
      department.save()
    
    defaults = {"is_head_of_department": True}
    staff, created = umodels.Staff.objects.update_or_create(
      user=head, specialization=head.specialization, defaults=defaults)
    return head
  except Exception as e:
    print("Exception geting head:" if not created else "Exception updating head staff model:", e)
    return None
  

# Generic Replacement for faculty_dean_helper and department_head_helper
def instance_role_helper(instance: Type[T] = None, role: Type[T] = None, 
                         _pre:bool = False, _type: str = None, *args, **kwargs) -> Optional[Type[T]]:
  """Update instance role and update or create the staff instance for role

  Args:
      instance (Type[T], optional): The instance to be updated. Defaults to None.
      role (Type[T], optional): The user to be set as role. Defaults to None.
      _pre (bool, optional): Is the function called before model .save(). Defaults to False.
      _type (str, optional): The type of instance: []. Defaults to None.

  Raises:
      Exception: None

  Returns:
      Optional[Type[T]]: The role user object
  """
  try:
    role = role if role else instance.role
    if not role.is_staff:
      raise Exception("Role User is not a staff")
    if not _pre:
      instance.role = role
      instance.save()
    
    defaults = {}
    if _type == 'faculty':
      defaults["is_dean_of_faculty"] = True
    elif _type == 'department':
      defaults["is_head_of_department"] = True
    
    staff, created = umodels.Staff.objects.update_or_create(
      user=role, specialization=role.specialization, defaults=defaults)
    return role
  except Exception as e:
    print(f"Exception geting {_type} role:" if not created else f"Exception updating {_type} role staff model:", e)
    return None
