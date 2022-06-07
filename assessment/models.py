from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from academics.models import Course
from user.models import Student

# Create your models here.


class Quiz(models.Model):
    """Model definition for Quiz."""

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    timer = models.IntegerField(default=15)
    max_score = models.IntegerField(default=10)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Quiz."""

        get_latest_by = "timestamp"
        ordering = ["-timestamp"]
        # ordering = ['id']
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        
    def save(self, *args, **kwargs):
        quiz = super(Quiz, self).save(*args, **kwargs)
        try:
            # related_students = self.course.specialization.student_set.all()
            related_course_registrations = self.course.courseregistration_set.all()
            print(f"related course registrations for created quiz:\n {related_course_registrations}")
            # for student in related_students:
            #     models.QuizTaker.objects.create(student=student, quiz=self)
            #     print(f"quiz taker created, student {student} registered for quiz {self}")
            for course_registration in related_course_registrations:
                try:
                    models.QuizTaker.objects.get(student=course_registration.student, quiz=self)
                except Exception:
                    models.QuizTaker.objects.create(student=course_registration.student, quiz=self)
                    print(f"quiz taker created, student {course_registration.student} registered for quiz {self}")
        except Exception:
            pass
        
        return quiz

    def __str__(self):
        """String representation of Quiz."""
        return self.name


class Question(models.Model):
    """Model definition for Question."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=250)
    file = models.FileField(
        verbose_name='answer_file',
        upload_to='files/quiz_answers/',
        blank=True, null=True
    )
    order = models.IntegerField(default=0)

    class Meta:
        """Meta definition for Question."""

        ordering = ['order']
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        """String representation of Question."""
        return self.label


class Answer(models.Model):
    """Model definition for Answer."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Answer."""

        ordering = ['id']
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        """String representation of Answer."""
        return self.text


class QuizTaker(models.Model):
    """Model definition for QuizTaker."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey("Grade", on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for QuizTaker."""

        ordering = ['id']
        verbose_name = _("QuizTaker")
        verbose_name_plural = _("QuizTakers")

    def __str__(self):
        """String representation of QuizTaker."""
        return f"{self.student}"

    def score(self):
        if self.grade:
            self.grade.max_score = self.quiz.max_score
            self.grade.save()
        else:
            self.grade = Grade.objects.create(max_score=self.quiz.max_score)

        score = 0
        if self.response_set.all():
            for response in self.response_set.all():
                if response.answer and (response.answer.is_correct is True):
                    score += 1

        if self.grade.score and (self.grade.score == score):
            return self.grade.score
        elif self.grade.score and (self.grade.score > 0):
            return self.grade.score
        else:
            self.grade.score = score
            self.grade.save()
            return self.grade.score

        return score


class Response(models.Model):
    """Model definition for Response."""

    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """Meta definition for Response."""

        ordering = ['id']
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        """String representation of Response."""
        return self.question.label


class Assignment(models.Model):
    """Model definition for Assignment."""

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    title = models.CharField(max_length=250)
    question = models.TextField(null=True, blank=True)
    # answer = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    file = models.FileField(
        verbose_name='answer_file',
        upload_to='files/assignment_questions/',
        blank=True, null=True
    )
    max_score = models.FloatField(default=10.00)
    due_date = models.DateTimeField()

    class Meta:
        """Meta definition for Assignment."""

        ordering = ['id']
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")

    def __str__(self):
        """String representation of Assignment."""
        return self.title


class AssignmentTaker(models.Model):
    """Model definition for QuizTaker."""

    student = models.ForeignKey(Student, related_name="assigned_asignments", on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name="assigned_asignments", on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey("Grade", on_delete=models.CASCADE, null=True, blank=True)
    score = models.FloatField(default=0.00)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for QuizTaker."""

        ordering = ['id']
        verbose_name = _("QuizTaker")
        verbose_name_plural = _("QuizTakers")

    def __str__(self):
        """String representation of QuizTaker."""
        return f"{self.student}"
    
    def is_passed(self):
        if self.score == 0.00 or not self.assignment.max_score:
            return False
        
        score_ratio = self.score/self.assignment.max_score
        if score_ratio >= 0.5:
            return True
        return False


class AssignmentResponse(models.Model):
    """Model definition for Response."""

    assignment_taker = models.ForeignKey(AssignmentTaker, related_name="assignment_responses", on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name="assignment_responses", on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    file = models.FileField(
        verbose_name='answer_file',
        upload_to='files/assignment_answers/',
        blank=True, null=True
    )

    class Meta:
        """Meta definition for Response."""

        ordering = ['id']
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        """String representation of Response."""
        return f"{self.assignment.title} - response"


class Grade(models.Model):
    """Model definition for Grade."""

    score = models.IntegerField(default=0, null=True, blank=True)
    max_score = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.BooleanField(default=False)
    update_reason = models.TextField(null=True, blank=True)
    update_timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for Grade."""

        ordering = ['id']
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')

    def __str__(self):
        """String representation of Grade."""
        return f"{self.score} of {self.max_score}"

    def get_value(self):
        try:
            if self.score / self.max_score >= 0.5:
                return 'Pass'
            elif self.score == 0:
                return "Not Available"
            else:
                return 'Fail'
        except Exception:
            return "Not Available"
        
    def get_grade(self):
        try:
            if self.score / 100.00 >= 0.9:
                return 'A+'
            elif self.score / 100.00 >= 0.8:
                return 'A'
            elif self.score / 100.00 >= 0.7:
                return 'B'
            elif self.score / 100.00 >= 0.6:
                return 'C'
            elif self.score / 100.00 >= 0.5:
                return 'D'
            elif self.score / 100.00 >= 0.4:
                return 'E'
            elif self.score == 0:
                return "Not Available"
            else:
                return 'F'
        except Exception:
            return None
