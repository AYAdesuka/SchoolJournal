from django.contrib import admin
from .models import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'middle_name')
    search_fields = ('user__username', 'last_name', 'first_name', 'middle_name')
    list_filter = ('user__is_active',)
    ordering = ('last_name', 'first_name')


@admin.register(ParentRelation)
class ParentRelationAdmin(admin.ModelAdmin):
    list_display = ('child_person', 'parent_person', 'relationship')
    search_fields = (
        'child_person__last_name',
        'child_person__first_name',
        'parent_person__last_name',
        'parent_person__first_name',
    )
    list_filter = ('relationship',)
    ordering = ('child_person__last_name', 'parent_person__last_name')


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'academic_year', 'class_teacher', 'status')
    search_fields = ('class_name',)
    list_filter = ('status', 'academic_year')
    ordering = ('academic_year', 'class_name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class', 'enrollment_date', 'departure_date')
    search_fields = ('student__last_name', 'student__first_name', 'school_class__class_name')
    list_filter = ('enrollment_date', 'departure_date')
    ordering = ('-enrollment_date',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'short_name', 'is_required')
    search_fields = ('subject_name', 'short_name')
    list_filter = ('is_required',)
    ordering = ('subject_name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('school_class', 'subject', 'teacher', 'day_of_week', 'lesson_number', 'room')
    search_fields = (
        'school_class__class_name',
        'subject__subject_name',
        'teacher__last_name',
        'teacher__first_name',
    )
    list_filter = ('day_of_week', 'school_class', 'subject', 'start_date', 'end_date')
    ordering = ('school_class__class_name', 'day_of_week', 'lesson_number')


@admin.register(SchoolPeriod)
class SchoolPeriodAdmin(admin.ModelAdmin):
    list_display = ('period_name', 'academic_year', 'period_number', 'is_current')
    search_fields = ('period_name', 'academic_year')
    list_filter = ('is_current', 'academic_year')
    ordering = ('-academic_year', 'period_number')


@admin.register(GradeBook)
class GradeBookAdmin(admin.ModelAdmin):
    list_display = ('school_class', 'subject', 'teacher', 'lesson_date', 'lesson_number', 'topic')
    search_fields = (
        'school_class__class_name',
        'subject__subject_name',
        'teacher__last_name',
        'teacher__first_name',
        'topic',
    )
    list_filter = ('lesson_date', 'school_class', 'subject')
    ordering = ('-lesson_date', 'lesson_number')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'gradebook', 'grade_value', 'grade_type', 'created_at')
    search_fields = (
        'student__last_name',
        'student__first_name',
        'grade_value',
    )
    list_filter = ('grade_type', 'gradebook__subject', 'created_at')
    ordering = ('-created_at',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'gradebook', 'attendance_status')
    search_fields = (
        'student__last_name',
        'student__first_name',
    )
    list_filter = ('attendance_status','gradebook__subject', 'gradebook__school_class')
    ordering = ()


@admin.register(FinalGrade)
class FinalGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'period', 'final_grade', 'approval_status', 'is_exam')
    search_fields = (
        'student__last_name',
        'student__first_name',
        'final_grade',
    )
    list_filter = ('approval_status', 'is_exam', 'subject', 'period')
    ordering = ('period', 'student__last_name')