from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.models import CustomUser
from journal.models import SchoolClass, Subject, GradeBook


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

    return render(request, 'class_gradebook.html', {'school_class': school_class})

@login_required
def class_subjects(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )
    print(Subject.objects.all())
    gradebooks = GradeBook.objects.filter(school_class=school_class).select_related('subject')

    return render(
        request,
        'sections/subjects.html',{'school_class': school_class,'gradebooks': gradebooks})

@login_required
def class_teachers(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/teachers.html', {'school_class': school_class})

@login_required
def class_grades(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/grades.html', {'school_class': school_class})

@login_required
def class_attendance(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/attendance.html', {'school_class': school_class})

@login_required
def class_stats(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/stats.html', {'school_class': school_class})

@login_required
def class_homework(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/homework.html', {'school_class': school_class})

@login_required
def class_docs(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/docs.html', {'school_class': school_class})

@login_required
def class_settings(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id,
        class_teacher=request.user
    )

    return render(request, 'sections/settings.html', {'school_class': school_class})

@login_required
def subject_grades(request, class_id, subject_id):

    school_class = get_object_or_404(SchoolClass,id=class_id, class_teacher=request.user)
    subject = get_object_or_404(Subject,id=subject_id)

    return render(request,'sections/subject_grades.html',{'school_class': school_class,'subject': subject,})