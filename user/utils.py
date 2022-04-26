from information.models import Notice, Information
from django.db.models import Q


def get_all_user_notices_depreciated(user):
  
  general_notices = Notice.objects.filter(scope__is_general=True)
  # print(f"general_notices: ${general_notices}")
  
  user_notices = general_notices
  # print(f"user_notices 1: ${user_notices}")
  
  print(user.student_set.all().first().specialization.max_level)
  print(user.student_set.all().first().academic_data.level)
  faculty_notices = Notice.objects.filter(scope__faculty=user.student_set.all().first().specialization.department.faculty)
  # print(f"faculty_notices: ${faculty_notices}")
  user_notices.union(faculty_notices)
  # print(f"user_notices 2: ${user_notices}")

  department_notices = Notice.objects.filter(scope__department=user.student_set.all().first().specialization.department)
  # print(f"department_notices: ${department_notices}")
  user_notices.union(department_notices)
  # print(f"user_notices 3: ${user_notices}")

  specialization_notices = Notice.objects.filter(scope__specialization=user.student_set.all().first().specialization)
  # print(f"specialization_notices: ${specialization_notices}")
  user_notices.union(specialization_notices)
  # print(f"user_notices 4: ${user_notices}")

  # TODO: Implement course_notices for courses not directly related to specialization

  level_notices = Notice.objects.filter(scope__level=user.student_set.all().first().academic_data.level)
  # print(f"level_notices: ${level_notices}")
  user_notices.union(level_notices)
  # print(f"user_notices 5: ${user_notices}")

  
  
  if user.student_set.all().first().academic_data.level.code == 100:
    first_year_notices = Notice.objects.filter(scope__is_first_year=True)
    # print(f"first_year_notices: ${first_year_notices}")
    user_notices.union(first_year_notices)
    # print(f"user_notices 6.1: ${user_notices}")
    
  if user.student_set.all().first().academic_data.level == user.student_set.all().first().specialization.max_level:
    final_year_notices = Notice.objects.filter(scope__is_final_year=True)
    print(f"final_year_notices: ${final_year_notices}")
    try:
      combined_user_notices = user_notices.union(final_year_notices)
      print(f"user_notices 6.2: ${combined_user_notices}")
    except Exception as e:
      print(e)
  
  all_notices = Notice.objects.all()
  # print(f"all_notices: ${len(all_notices)}")
  
  for notice in all_notices:
    # if notice.scope.is_general:
    #   pass
    
    if notice.scope.course in user.student_set.all().first().specialization.course_set.all():
      course_notices = Notice.objects.filter(scope__course=notice.scope.course)
      # print(f"course_notices: ${course_notices}")
      user_notices.union(course_notices)
  
  print(f"user_notices: ${user_notices}")
  return user_notices


def get_all_user_notices(user):
    
  if user.student_set.all().first().academic_data.level.code == 100:
    user_notice = Notice.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__is_first_year=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_notice_first_year: ${user_notice}")
    
  elif user.student_set.all().first().academic_data.level == user.student_set.all().first().specialization.max_level:
    user_notice = Notice.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__is_final_year=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_notice_final_year: ${user_notice}")
    
  else:
    user_notice = Notice.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_notice: ${user_notice}")
    
  return user_notice


def get_all_user_information(user):
    
  if user.student_set.all().first().academic_data.level.code == 100:
    user_information = Information.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__is_first_year=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_information_first_year: ${user_information}")
    
  elif user.student_set.all().first().academic_data.level == user.student_set.all().first().specialization.max_level:
    user_information = Information.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__is_final_year=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_information_final_year: ${user_information}")
    
  else:
    user_information = Information.objects.filter(
      Q(scope__is_general=True) |
      Q(scope__faculty=user.student_set.all().first().specialization.department.faculty) |
      Q(scope__department=user.student_set.all().first().specialization.department) |
      Q(scope__specialization=user.student_set.all().first().specialization) |
      Q(scope__level=user.student_set.all().first().academic_data.level) |
      Q(scope__course__in=user.student_set.all().first().specialization.course_set.all())
    )
    # print(f"user_information: ${user_information}")
    
  return user_information
  