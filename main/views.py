from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser
from journal.models import SchoolClass, Enrollment, GradeBook, Grade
from django.http import JsonResponse


def home(request):
    context = {
        'students_count': CustomUser.objects.count(),
        'classes_count': SchoolClass.objects.count(),
        'teachers_count': CustomUser.objects.filter(role='учитель').count(),
    }
    return render(request, 'home.html', context)


@login_required
def gradebook(request):
    classes = request.user.class_teacher_classes.all()

    return render(request,'gradebook.html',{'classes': classes})


@login_required
def class_gradebook(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    grade_map = {}

    for g in Grade.objects.filter(gradebook__school_class=school_class):
        grade_map[(g.student_id, g.gradebook_id)] = g.grade_value

    GRADE_CHOICES = [1, 2, 3, 4, 5]

    enrollments = (
        Enrollment.objects
        .filter(school_class=school_class)
        .select_related('student')
        .order_by('student__last_name', 'student__first_name')
    )

    lessons = (
        GradeBook.objects
        .filter(school_class=school_class)
        .select_related('subject')
        .order_by('lesson_date', 'lesson_number')
    )

    student_rows = []

    for enrollment in enrollments:
        student = enrollment.student

        row = {
            'student': student,
            'grades': []
        }

        for lesson in lessons:
            grade = Grade.objects.filter(
                student=student,
                gradebook=lesson
            ).first()

            row['grades'].append(
                grade.grade_value if grade else ''
            )

        student_rows.append(row)

    return render(request, 'class_gradebook.html', {
        'school_class': school_class,
        'enrollments': enrollments,
        'lessons': lessons,
        'grade_map': grade_map,
        'grades': [1, 2, 3, 4, 5],
    })


@login_required
def update_grade(request):
    if request.method == "POST":

        student_id = request.POST.get("student_id")
        gradebook_id = request.POST.get("gradebook_id")
        grade_value = request.POST.get("grade_value")

        gradebook = get_object_or_404(GradeBook, id=gradebook_id)
        student = get_object_or_404(CustomUser, id=student_id)

        if not grade_value:
            Grade.objects.filter(
                student=student,
                gradebook=gradebook
            ).delete()
            return redirect(request.META.get("HTTP_REFERER"))

        Grade.objects.update_or_create(
            student=student,
            gradebook=gradebook,
            defaults={"grade_value": grade_value}
        )

        return redirect(request.META.get("HTTP_REFERER"))