from typing import Type, TypeVar, Optional
from django.db.models import Q
from user import models
from datetime import datetime


def queryset_attrs(queryset, attribute, seperator: str = " ", index: int = 1) -> list:
  formatted_attribute = attribute.split(sep)[index] if seperator and index else attribute
  attrs = [int(formatted_attribute) for x in queryset]
  return attrs

def max_custom_id(array: list):
  return max(array)

def next_id(id):
  return int(id) + 1

def create_id(id, prefix: str = "STU", length: int = 5, seperator: str = " "):
  str_id = str(id).zfill(length)
  return f"{prefix}{seperator}{str_id}"


def set_id(queryset, instance, attribute, custom_id):
  filtered_qs = queryset.filter(Q(code=custom_id) or Q(student_id=custom_id) or Q(matric_no=custom_id) or Q(employee_id=custom_id))
  if not filtered_qs:
    # # NOTE: commented code does not work
    # attribute = custom_id
    # instance.save()
    return custom_id
  return None


def custom_id(queryset, instance, attribute, prefix: str = "STU", length: int = 5, seperator: str = " ", index: int = 1):
  try:
    id_list = queryset_attrs(queryset, attribute, seperator, index)
    id = next_id(id = max_custom_id(id_list))
  except Exception:
    id = len(queryset)  # + 1
  return set_id(queryset, instance, attribute, create_id(id, prefix, length, seperator))
