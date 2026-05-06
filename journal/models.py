from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ParentRelation(models.Model):
    RELATION_CHOICES = [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]

    child_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='child_relations'
    )
    parent_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='parent_relations'
    )
    relationship = models.CharField(max_length=20, choices=RELATION_CHOICES)

    def __str__(self):
        return f'{self.parent_person} -> {self.child_person}'

    class Meta:
        ordering = ['parent_person', 'child_person']
        verbose_name = 'Родители'
        verbose_name_plural = 'Родители'



class SchoolClass(models.Model):
    CLASS_STATUS_CHOICES = [
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('archived', 'Archived'),
    ]

    class_name = models.CharField(max_length=20, unique=True)
    academic_year = models.CharField(max_length=9)
    class_teacher = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_teacher_classes'
    )
    room_number = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CLASS_STATUS_CHOICES, default='active')

    def __str__(self):
        return self.class_name

    class Meta:
        ordering = ['class_name']
        verbose_name = 'Школьный класс'
        verbose_name_plural = 'Школьные классы'


class Enrollment(models.Model):
    student = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateField()
    departure_order = models.CharField(max_length=50, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    departure_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.student} -> {self.school_class}'

    class Meta:
        ordering = ['departure_order', 'departure_date']
        verbose_name = 'Зачисление'
        verbose_name_plural = 'Зачисления'


class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    hours_per_year = models.PositiveIntegerField()
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ['subject_name']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Schedule(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, 'Monday'
        TUESDAY = 2, 'Tuesday'
        WEDNESDAY = 3, 'Wednesday'
        THURSDAY = 4, 'Thursday'
        FRIDAY = 5, 'Friday'
        SATURDAY = 6, 'Saturday'
        SUNDAY = 7, 'Sunday'

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    teacher = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='teacher_schedules'
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DayOfWeek.choices)
    lesson_number = models.PositiveSmallIntegerField()
    room = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.school_class} - {self.subject}'

    class Meta:
        ordering = ['school_class', 'subject', 'teacher', 'day_of_week']
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'



class SchoolPeriod(models.Model):
    period_name = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=9)
    period_number = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.period_name} {self.academic_year}'

    class Meta:
        ordering = ['period_name', 'academic_year']
        verbose_name = 'Учебный период'
        verbose_name_plural = 'Учебный период'


class GradeBook(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='gradebooks'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='gradebooks'
    )
    teacher = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='gradebooks'
    )
    lesson_date = models.DateField()
    lesson_number = models.PositiveSmallIntegerField()
    topic = models.TextField(blank=True, null=True)
    homework = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.school_class} - {self.subject} - {self.lesson_date}'

    class Meta:
        ordering = ['school_class', 'subject', 'teacher', 'lesson_date']
        verbose_name = 'Журнал успеваемости'
        verbose_name_plural = 'Журналы успеваемости'


class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('lesson', 'Lesson'),
        ('homework', 'Homework'),
        ('control', 'Control'),
        ('project', 'Project'),
        ('oral', 'Oral'),
    ]

    gradebook = models.ForeignKey(
        GradeBook,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    student = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    grade_value = models.CharField(max_length=10)
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES, default='lesson')
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.grade_value}'

    class Meta:
        ordering = ['student', 'grade_value']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    gradebook = models.ForeignKey(
        GradeBook,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    student = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES)
    reason = models.CharField(max_length=100, blank=True, null=True)
    doctor_note = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.student} - {self.attendance_status}'

    class Meta:
        ordering = ['student', 'attendance_status']
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемости'


class FinalGrade(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('published', 'Published'),
    ]

    student = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='final_grades'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='final_grades'
    )
    period = models.ForeignKey(
        SchoolPeriod,
        on_delete=models.CASCADE,
        related_name='final_grades'
    )
    final_grade = models.CharField(max_length=10)
    calculated_grade = models.CharField(max_length=10, blank=True, null=True)
    is_exam = models.BooleanField(default=False)
    teacher_comment = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.final_grade}'

    class Meta:
        ordering = ['student', 'final_grade']
        verbose_name = 'Итоговая оценка'
        verbose_name_plural = 'Итоговые оценки'