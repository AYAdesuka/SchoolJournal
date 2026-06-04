from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('gradebook/', views.gradebook, name='gradebook'),
    path('gradebook/<int:class_id>/', views.class_gradebook, name='class_gradebook'),
    path('save-grade/', views.save_grade, name='safe_grade'),
    path('schedule/', views.class_schedule, name='schedule'),
    path('schedule/<int:class_id>/', views.class_schedule, name='class_schedule'),
    path('class/<int:class_id>/settings/', views.class_settings, name='class_settings'),
    path('class/<int:class_id>/student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('class/<int:class_id>/add-subject/', views.add_subject_to_class, name='add_subject_to_class')
]
