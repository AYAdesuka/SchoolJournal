from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.db.models import Q
from datetime import date
from .forms import SubjectForm


from accounts.models import CustomUser
from journal.models import SchoolClass, Enrollment, GradeBook, Grade, Subject, Schedule

def home(request):
    school_class = SchoolClass.objects.first()
    context = {
        'school_class': school_class,
        'students_count': CustomUser.objects.count(),
        'classes_count': SchoolClass.objects.count(),
        'teachers_count': CustomUser.objects.filter(role='учитель').count(),
    }
    return render(request, 'home.html', context)

@login_required
def gradebook(request):
    user = request.user
    if user.role in ['teacher', 'учитель']:
        target = SchoolClass.objects.filter(Q(class_teacher=user) | Q(gradebooks__teacher=user)).distinct().first()
    elif user.role in ['student', 'студент']:
        enr = Enrollment.objects.filter(student=user).first()
        target = enr.school_class if enr else None
    else:
        target = SchoolClass.objects.first()

    if target:
        return redirect('main:class_gradebook', class_id=target.id)
    return render(request, 'class_gradebook.html', {'message': 'Классы не найдены'})

@login_required
def class_gradebook(request, class_id=None):
    if not class_id:
        return redirect('main:gradebook')

    user = request.user

    if user.role in ['teacher', 'учитель']:
        my_classes = SchoolClass.objects.filter(Q(class_teacher=user) | Q(gradebooks__teacher=user)).distinct()
    elif user.is_superuser:
        my_classes = SchoolClass.objects.all()
    else:
        my_classes = SchoolClass.objects.filter(enrollments__student=user).distinct()

    school_class = get_object_or_404(SchoolClass, id=class_id)

    enrollments = Enrollment.objects.filter(school_class=school_class).select_related('student')
    if user.role in ['student', 'студент']:
        enrollments = enrollments.filter(student=user)

    subject_id = request.GET.get('subject')
    lessons = GradeBook.objects.filter(school_class=school_class)
    if subject_id:
        lessons = lessons.filter(subject_id=subject_id)
    lessons = lessons.order_by('lesson_date', 'lesson_number')

    grades_query = Grade.objects.filter(gradebook__in=lessons)

    if user.role in ['student', 'студент']:
        stats_grades = grades_query.filter(student=user)
    else:
        stats_grades = grades_query

    grade_map = {f"{g.student_id}_{g.gradebook_id}": str(g.grade_value) for g in grades_query}

    numeric_values = []
    absences_count = 0

    for g in stats_grades:
        val = str(g.grade_value).strip()
        if val.isdigit():
            numeric_values.append(int(val))
        elif val.upper() == 'Н' or val.upper() == 'H':
            absences_count += 1

    if numeric_values:
        avg_grade = round(sum(numeric_values) / len(numeric_values), 2)
    else:
        avg_grade = 0.0

    context = {

        'my_classes': my_classes,
        'school_class': school_class,
        'enrollments': enrollments,
        'lessons': lessons,
        'grade_map': grade_map,
        'selected_subject': subject_id,
        'grades': ['5', '4', '3', '2', 'Н'],
        'all_subjects': Subject.objects.all(),
        'avg_grade': avg_grade,
        'absences': absences_count,
    }
    return render(request, 'class_gradebook.html', context)

@login_required
def schedule(request):
    user = request.user
    if user.role in ['teacher', 'учитель']:
        target = SchoolClass.objects.filter(Q(class_teacher=user) | Q(schedules__teacher=user)).distinct().first()
    elif user.role in ['student', 'студент']:
        enr = Enrollment.objects.filter(student=user).first()
        target = enr.school_class if enr else None
    else:
        target = SchoolClass.objects.first()

    if target:
        return redirect('main:class_schedule', class_id=target.id)
    return render(request, 'schedule.html', {'message': 'Расписание не найдено'})

@login_required
def class_schedule(request, class_id=None):
    user = request.user

    if not class_id:
        if user.role in ['teacher', 'учитель']:
            target = SchoolClass.objects.filter(
                Q(class_teacher=user) | Q(schedules__teacher=user)
            ).distinct().first()
        elif user.role in ['student', 'студент']:
            enr = Enrollment.objects.filter(student=user).first()
            target = enr.school_class if enr else None
        else:
            target = SchoolClass.objects.first()

        if target:
            return redirect('main:class_schedule', class_id=target.id)
        return render(request, 'schedule.html', {'message': 'Расписание не найдено'})

    if user.role in ['teacher', 'учитель']:
        my_classes = SchoolClass.objects.filter(
            Q(class_teacher=user) | Q(schedules__teacher=user)
        ).distinct()
    elif user.is_superuser:
        my_classes = SchoolClass.objects.all()
    else:
        my_classes = SchoolClass.objects.filter(enrollments__student=user).distinct()

    school_class = get_object_or_404(my_classes, id=class_id)

    can_edit = user.is_superuser or school_class.class_teacher == user
    is_edit = (request.GET.get('edit') == '1') and can_edit

    if request.method == 'POST' and is_edit:
        Schedule.objects.filter(school_class=school_class).delete()
        days_map = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница'}

        for day_num, day_name in days_map.items():
            for num in range(1, 7):
                subj_id = request.POST.get(f'subject_{day_name}_{num}')
                room_val = request.POST.get(f'room_{day_name}_{num}')
                if subj_id:
                    Schedule.objects.create(
                        school_class=school_class,
                        subject_id=subj_id,
                        teacher=user,
                        day_of_week=day_num,
                        lesson_number=num,
                        room=room_val,
                        start_date=date.today()
                    )
        return redirect('main:class_schedule', class_id=school_class.id)

    days_map = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница'}
    entries = Schedule.objects.filter(school_class=school_class).select_related('subject')

    weekly_schedule = {name: [] for name in days_map.values()}
    for d_num, d_name in days_map.items():
        for n in range(1, 7):
            e = next((x for x in entries if x.day_of_week == d_num and x.lesson_number == n), None)
            weekly_schedule[d_name].append({
                'number': n,
                'subject_id': e.subject_id if e else None,
                'subject_name': e.subject.subject_name if e else '',
                'room': e.room if e else ''
            })

    context = {
        'my_classes': my_classes,
        'school_class': school_class,
        'weekly_schedule': weekly_schedule,
        'is_edit': is_edit,
        'can_edit': can_edit,
        'all_subjects': Subject.objects.all().order_by('subject_name'),
    }
    return render(request, 'schedule.html', context)

@login_required
def save_grade(request):
    if request.method == 'POST':
        if request.user.role not in ['teacher', 'учитель'] and not request.user.is_superuser:
            return HttpResponseForbidden()

        student_id = request.POST.get('student_id')
        gradebook_id = request.POST.get('gradebook_id')
        grade_value = request.POST.get('grade_value')

        Grade.objects.update_or_create(
            student_id=student_id,
            gradebook_id=gradebook_id,
            defaults={'grade_value': grade_value}
        ) if grade_value else Grade.objects.filter(student_id=student_id, gradebook_id=gradebook_id).delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('main:home')

@login_required
def class_settings(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id, class_teacher=request.user)
    students = CustomUser.objects.filter(enrollments__school_class=school_class).order_by('last_name')

    if request.method == 'POST':
        pass

    context = {'school_class': school_class, 'students': students}
    return render(request, 'class_settings.html', context)

@login_required
def delete_student(request, class_id, student_id):
    school_class = get_object_or_404(SchoolClass, id=class_id, class_teacher=request.user)
    if request.method == 'POST':
        Enrollment.objects.filter(school_class=school_class, student_id=student_id).delete()
    return redirect('main:class_settings', class_id=class_id)


@login_required
def add_subject(request):
    if request.user.role not in ['teacher', 'учитель', 'admin']:
        messages.error(request, 'У вас нет прав для добавления предметов')
        return redirect('main:gradebook')

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предмет успешно добавлен')
            return redirect('main:gradebook')
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form})


@login_required
def add_subject_to_class(request, class_id):
    if request.user.role not in ['teacher', 'учитель', 'admin']:
        messages.error(request, 'У вас нет прав для добавления предметов')
        return redirect('main:gradebook')

    school_class = get_object_or_404(SchoolClass, id=class_id)

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            # Создаем журнал успеваемости для этого класса и предмета
            GradeBook.objects.create(
                school_class=school_class,
                subject=subject,
                teacher=request.user,
                lesson_number=1
            )
            messages.success(request, f'Предмет "{subject.subject_name}" добавлен в класс {school_class.class_name}')
            return redirect('main:class_gradebook', class_id=class_id)
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form, 'school_class': school_class})