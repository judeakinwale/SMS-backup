from information.models import Notice, Information
from django.db.models import Q


def get_all_user_notices_depreciated(user):
  
  general_notices = Notice.objects.filter(scope__is_general=True)
  
  user_notices = general_notices
  
  print(user.student_set.all().first().specialization.max_level)
  print(user.student_set.all().first().academic_data.level)
  faculty_notices = Notice.objects.filter(scope__faculty=user.student_set.all().first().specialization.department.faculty)
  user_notices.union(faculty_notices)

  department_notices = Notice.objects.filter(scope__department=user.student_set.all().first().specialization.department)
  user_notices.union(department_notices)

  specialization_notices = Notice.objects.filter(scope__specialization=user.student_set.all().first().specialization)
  user_notices.union(specialization_notices)

  # TODO: Implement course_notices for courses not directly related to specialization

  level_notices = Notice.objects.filter(scope__level=user.student_set.all().first().academic_data.level)
  user_notices.union(level_notices)

  if user.student_set.all().first().academic_data.level.code == 100:
    first_year_notices = Notice.objects.filter(scope__is_first_year=True)
    user_notices.union(first_year_notices)
    
  if user.student_set.all().first().academic_data.level == user.student_set.all().first().specialization.max_level:
    final_year_notices = Notice.objects.filter(scope__is_final_year=True)
    user_notices.union(final_year_notices)
  
  all_notices = Notice.objects.all()
  
  for notice in all_notices:
    if notice.scope.course in user.student_set.all().first().specialization.course_set.all():
      course_notices = Notice.objects.filter(scope__course=notice.scope.course)
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
