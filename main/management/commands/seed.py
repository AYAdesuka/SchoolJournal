import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from accounts.models import CustomUser
from journal.models import (
    Attendance,
    FinalGrade,
    Grade,
    GradeBook,
    ParentRelation,
    SchoolClass,
    SchoolPeriod,
    Schedule,
    Subject,
    Enrollment,
)


class Command(BaseCommand):
    help = 'Заполнение школьного журнала тестовыми данными'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')

        teachers_data = [
            ('Иванов', 'Алексей', 'Петрович'),
            ('Смирнова', 'Елена', 'Игоревна'),
            ('Кузнецов', 'Дмитрий', 'Сергеевич'),
            ('Попова', 'Анна', 'Викторовна'),
            ('Соколов', 'Олег', 'Андреевич'),
        ]

        students_data = [
            ('Петров', 'Илья', 'Алексеевич'),
            ('Сидорова', 'Мария', 'Денисовна'),
            ('Волков', 'Никита', 'Максимович'),
            ('Лебедева', 'Дарья', 'Олеговна'),
            ('Новиков', 'Артём', 'Игоревич'),
            ('Морозова', 'Полина', 'Сергеевна'),
            ('Козлов', 'Егор', 'Владимирович'),
            ('Фёдорова', 'Алина', 'Романовна'),
        ]

        period, _ = SchoolPeriod.objects.get_or_create(
            period_name='1 четверть',
            academic_year='2025-2026',
            period_number=1,
            defaults={
                'start_date': timezone.now().date() - timedelta(days=60),
                'end_date': timezone.now().date() - timedelta(days=1),
                'is_current': True,
            }
        )

        subjects_data = [
            ('Математика', 'МАТ', 170, True),
            ('Русский язык', 'РУС', 140, True),
            ('Литература', 'ЛИТ', 102, True),
            ('История', 'ИСТ', 68, True),
            ('Биология', 'БИО', 68, True),
            ('География', 'ГЕО', 68, True),
            ('Информатика', 'ИНФ', 68, True),
            ('Английский язык', 'АНГ', 102, True),
            ('Физкультура', 'ФК', 68, True),
            ('ИЗО', 'ИЗО', 34, False),
        ]

        classes_data = [
            '1 А', '2 А', '3 А', '4 А', '5 А',
            '6 А', '7 А', '8 А', '9 А', '10 А', '11 А'
        ]

        teacher_users = []
        for last_name, first_name, middle_name in teachers_data:
            user, _ = CustomUser.objects.get_or_create(
                username=f'{last_name.lower()}_{first_name.lower()}',
                defaults={
                    'role': 'учитель',
                    'last_name': last_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'birth_date': fake.date_of_birth(minimum_age=25, maximum_age=65),
                    'phone': fake.phone_number(),
                    'address': fake.address(),
                }
            )
            teacher_users.append(user)

        student_users = []
        for last_name, first_name, middle_name in students_data:
            user, _ = CustomUser.objects.get_or_create(
                username=f'{last_name.lower()}_{first_name.lower()}',
                defaults={
                    'role': 'студент',
                    'last_name': last_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'birth_date': fake.date_of_birth(minimum_age=7, maximum_age=17),
                    'phone': fake.phone_number(),
                    'address': fake.address(),
                }
            )
            student_users.append(user)

        subjects = []
        for subject_name, short_name, hours_per_year, is_required in subjects_data:
            subject, _ = Subject.objects.get_or_create(
                subject_name=subject_name,
                defaults={
                    'short_name': short_name,
                    'description': fake.text(max_nb_chars=150),
                    'hours_per_year': hours_per_year,
                    'is_required': is_required,
                }
            )
            subjects.append(subject)

        school_classes = []
        for class_name in classes_data:
            school_class, _ = SchoolClass.objects.get_or_create(
                class_name=class_name,
                defaults={
                    'academic_year': period,
                    'class_teacher': random.choice(teacher_users),
                    'room_number': str(random.randint(101, 409)),
                    'start_date': period.start_date,
                    'end_date': period.end_date,
                    'status': 'active',
                }
            )
            school_classes.append(school_class)

        for student in student_users:
            school_class = random.choice(school_classes)
            Enrollment.objects.get_or_create(
                student=student,
                school_class=school_class,
                defaults={
                    'enrollment_date': period.start_date,
                    'departure_order': None,
                    'departure_date': None,
                    'departure_reason': None,
                }
            )

        for student in student_users:
            parent, _ = CustomUser.objects.get_or_create(
                username=f'parent_{student.username}',
                defaults={
                    'role': 'админ',
                    'last_name': fake.last_name(),
                    'first_name': fake.first_name(),
                    'middle_name': fake.first_name_male(),
                    'birth_date': fake.date_of_birth(minimum_age=30, maximum_age=55),
                    'phone': fake.phone_number(),
                    'address': fake.address(),
                }
            )
            ParentRelation.objects.get_or_create(
                child_person=student,
                parent_person=parent,
                defaults={'relationship': random.choice(['мама', 'папа', 'опекун', 'Другое'])}
            )

        for school_class in school_classes:
            for subject in random.sample(subjects, k=min(6, len(subjects))):
                teacher = random.choice(teacher_users)
                for day in [1, 2, 3, 4, 5]:
                    Schedule.objects.get_or_create(
                        school_class=school_class,
                        subject=subject,
                        teacher=teacher,
                        day_of_week=day,
                        lesson_number=random.randint(1, 7),
                        defaults={
                            'room': str(random.randint(101, 409)),
                            'start_date': period.start_date,
                            'end_date': period.end_date,
                        }
                    )

        for school_class in school_classes:
            class_students = random.sample(student_users, k=min(len(student_users), 5))
            class_subjects = random.sample(subjects, k=min(len(subjects), 4))

            for subject in class_subjects:
                teacher = random.choice(teacher_users)

                for offset in range(5):
                    lesson_date = period.start_date + timedelta(days=offset * 7)
                    gradebook = GradeBook.objects.create(
                        school_class=school_class,
                        subject=subject,
                        teacher=teacher,
                        lesson_date=lesson_date,
                        lesson_number=random.randint(1, 7),
                        topic=fake.sentence(nb_words=6),
                        homework=fake.sentence(nb_words=8),
                        notes=fake.sentence(nb_words=5),
                    )

                    for student in class_students:
                        Attendance.objects.create(
                            gradebook=gradebook,
                            student=student,
                            attendance_status=random.choice(
                                ['present', 'present', 'present', 'late', 'absent', 'excused']),
                            reason=fake.word() if random.choice([True, False]) else None,
                            doctor_note=random.choice([True, False]),
                            notes=fake.sentence(nb_words=6) if random.choice([True, False]) else None,
                        )

                        Grade.objects.create(
                            gradebook=gradebook,
                            student=student,
                            grade_value=random.choice(['2', '3', '4', '5']),
                            grade_type=random.choice(['lesson', 'homework', 'control', 'project', 'oral']),
                            weight=random.choice(['1.00', '1.00', '1.50', '2.00']),
                            comment=fake.sentence(nb_words=4) if random.choice([True, False]) else None,
                        )

                    for student in class_students:
                        FinalGrade.objects.get_or_create(
                            student=student,
                            subject=subject,
                            period=period,
                            defaults={
                                'final_grade': random.choice(['3', '4', '5']),
                                'calculated_grade': random.choice(['3', '4', '5']),
                                'is_exam': random.choice([True, False]),
                                'teacher_comment': fake.sentence(nb_words=8),
                                'approval_status': random.choice(['draft', 'approved', 'published']),
                            }
                        )

        self.stdout.write(self.style.SUCCESS('Школьный журнал успешно заполнен'))