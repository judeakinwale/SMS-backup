import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from django.utils import timezone
from user import models as umodels
from information import models as imodels
from assessment import models as amodels
from academics import models as acmodels


def sample_user(email='test@email.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


def sample_scope(description='test', **kwargs):
    return imodels.Scope.objects.create(description=description, **kwargs)


class ModelTest(TestCase):

    def setUp(self):
        self.user = sample_user()

    def test_create_user_with_email_successful(self):
        """test creating a user with email is successful"""
        email = 'test@gmail.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        """test that the new user email is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email,
            'testpass'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating new user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'testpass'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_staff_str(self):
        """test the staff str representation"""
        staff = umodels.Staff.objects.create(
            user=self.user,
            employee_id=1,
        )
        self.assertEqual(str(staff), str(staff.employee_id))

    def test_student_str(self):
        """test the student str representation"""
        student = umodels.Student.objects.create(
            user=self.user,
            matric_no=23412322,
            student_id=1,
        )
        self.assertEqual(str(student), f"{student.matric_no or student.student_id}")

    def test_biodata_str(self):
        """test the biodata str representation"""
        biodata = umodels.Biodata.objects.create(user=self.user)
        if biodata.user.last_name and biodata.first_name:
            self.assertEqual(str(biodata), f"{biodata.user.last_name}  {biodata.user.first_name}")
        else:
            self.assertEqual(str(biodata), biodata.user.email)

    def test_academic_data_str(self):
        """test the academic_data str representation"""
        student = umodels.Student.objects.create(
            user=self.user,
            matric_no=23412322,
            student_id=1,
        )
        faculty = acmodels.Faculty.objects.create(name="Test Faculty")
        level = acmodels.Level.objects.create(code=500)
        department = acmodels.Department.objects.create(
            faculty=faculty,
            name="Test Faculty",
        )
        programme = acmodels.Programme.objects.create(
            department=department,
            name="Test Programme",
            code=1,
            max_level=level,
        )
        academic_data = umodels.AcademicData.objects.create(
            student=student,
            programme=programme,
            start_date=timezone.now(),
        )
        self.assertEqual(
            str(academic_data),
            f"{academic_data.student.matric_no or academic_data.student.student_id}"
        )

    def test_academic_history_str(self):
        """test the academic_history str representation"""
        biodata = umodels.Biodata.objects.create(user=self.user)
        academic_history = umodels.AcademicHistory.objects.create(
            biodata=biodata,
        )
        if academic_history.biodata.user.last_name and academic_history.biodata.first_name:
            self.assertEqual(
                str(academic_history.biodata),
                f"{academic_history.biodata.user.last_name}  {academic_history.biodata.user.first_name}"
            )
        else:
            self.assertEqual(str(academic_history.biodata), academic_history.biodata.user.email)

    def test_health_data_str(self):
        """test the health_data str representation"""
        biodata = umodels.Biodata.objects.create(user=self.user)
        health_data = umodels.HealthData.objects.create(
            biodata=biodata,
        )
        if health_data.biodata.user.last_name and health_data.biodata.first_name:
            self.assertEqual(
                str(health_data.biodata),
                f"{health_data.biodata.user.last_name}  {health_data.biodata.user.first_name}"
            )
        else:
            self.assertEqual(str(health_data.biodata), health_data.biodata.user.email)

    def test_family_data_str(self):
        """test the family_data str representation"""
        biodata = umodels.Biodata.objects.create(user=self.user)
        family_data = umodels.FamilyData.objects.create(
            biodata=biodata,
        )
        if family_data.biodata.user.last_name and family_data.biodata.first_name:
            self.assertEqual(
                str(family_data.biodata),
                f"{family_data.biodata.user.last_name}  {family_data.biodata.user.first_name}"
            )
        else:
            self.assertEqual(str(family_data.biodata), family_data.biodata.user.email)

    def test_course_registration_str(self):
        """test the course_registration str representation"""
        student = umodels.Student.objects.create(
            user=self.user,
            matric_no=23412322,
            student_id=1,
        )
        faculty = acmodels.Faculty.objects.create(name="Test Faculty")
        level = acmodels.Level.objects.create(code=500)
        department = acmodels.Department.objects.create(
            faculty=faculty,
            name="Test Faculty",
        )
        programme = acmodels.Programme.objects.create(
            department=department,
            name="Test Programme",
            code=1,
            max_level=level,
        )
        course = acmodels.Course.objects.create(
            programme=programme,
            name="Test Course"
        )
        course_registration = umodels.CourseRegistration.objects.create(
            student=student,
            course=course,
        )
        self.assertEqual(str(course_registration), f"{course_registration.course.name} - registration")

    def test_scope_str(self):
        """test the scope str representation"""
        scope = imodels.Scope.objects.create(
            description='Test'
        )
        self.assertEqual(str(scope), scope.description)

    def test_information_str(self):
        """test the information str representation"""
        information = imodels.Information.objects.create(
            source=self.user,
            scope=sample_scope(),
            title='Test title',
            body='some test text'
        )
        expected_str = f"{information.title} for {information.scope}"
        self.assertEqual(str(information), expected_str)

    def test_notice_str(self):
        """test the notice str representation"""
        notice = imodels.Notice.objects.create(
            source=self.user,
            scope=sample_scope(),
            title='Test title',
            message='This is a test notice'
        )
        self.assertEqual(str(notice), notice.title)

    def test_information_image_str(self):
        """test the information image str representation"""
        information = imodels.Information.objects.create(
            source=self.user,
            scope=sample_scope(),
            title='Test title',
            body='some test text with an image'
        )
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            info_img = imodels.InformationImage.objects.create(
                information=information,
                image=ntf.name,
                description="A blue 10px image"
            )

        self.assertEqual(str(info_img), info_img.description)

    def test_quiz_str(self):
        """test the quiz str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        self.assertEqual(str(quiz), quiz.name)

    def test_question_str(self):
        """test the question str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        question = amodels.Question.objects.create(
            quiz=quiz,
            label='Test title',
        )
        self.assertEqual(str(question), question.label)

    def test_answer_str(self):
        """test the answer str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        question = amodels.Question.objects.create(
            quiz=quiz,
            label='Test title',
        )
        answer = amodels.Answer.objects.create(
            question=question,
            text='some answer text',
        )
        self.assertEqual(str(answer), answer.text)

    def test_quiz_taker_str(self):
        """test the quiz_taker str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        quiz_taker = amodels.QuizTaker.objects.create(
            student=self.user,
            quiz=quiz,
        )
        self.assertEqual(str(quiz_taker), str(quiz_taker.student))

    def test_response_str(self):
        """test the response str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        quiz_taker = amodels.QuizTaker.objects.create(
            student=self.user,
        )
        question = amodels.Question.objects.create(
            quiz=quiz,
            label='Test title',
        )
        answer = amodels.Answer.objects.create(
            question=question,
            text='some answer text',
        )
        response = amodels.Response.objects.create(
            quiz_taker=quiz_taker,
            question=question,
            answer=answer,
        )
        self.assertEqual(str(response), response.question.label)

    def test_grade_str(self):
        """test the grade str representation"""
        grade = amodels.Grade.objects.create(
            max_score=20,
        )
        self.assertEqual(str(grade), f"{grade.score} of {grade.max_score}")

    def test_faculty_str(self):
        """test the faculty str representation"""
        faculty = acmodels.Faculty.objects.create(
            name="Test Faculty",
            code=1,
        )
        self.assertEqual(str(faculty), faculty.name)

    def test_level_str(self):
        """test the level str representation"""
        level = acmodels.Level.objects.create(code=400)
        self.assertEqual(str(level), str(level.code))

    def test_department_str(self):
        """test the department str representation"""
        faculty = acmodels.Faculty.objects.create(name="Test Faculty")
        department = acmodels.Department.objects.create(
            faculty=faculty,
            name="Test Department",
            code=1,
        )
        self.assertEqual(str(department), department.name)

    def test_programme_str(self):
        """test the programme str representation"""
        faculty = acmodels.Faculty.objects.create(name="Test Faculty")
        level = acmodels.Level.objects.create(code=500)
        department = acmodels.Department.objects.create(
            faculty=faculty,
            name="Test Faculty",
        )
        programme = acmodels.Programme.objects.create(
            department=department,
            name="Test Programme",
            code=1,
            max_level=level,
        )
        self.assertEqual(str(programme), programme.name)

    def test_course_str(self):
        """test the course str representation"""
        faculty = acmodels.Faculty.objects.create(name="Test Faculty")
        level = acmodels.Level.objects.create(code=500)
        department = acmodels.Department.objects.create(
            faculty=faculty,
            name="Test Faculty",
        )
        programme = acmodels.Programme.objects.create(
            department=department,
            name="Test Programme",
            code=1,
            max_level=level,
        )
        course = acmodels.Course.objects.create(
            programme=programme,
            name="Test Course"
        )
        self.assertEqual(str(course), course.name)
