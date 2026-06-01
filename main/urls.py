from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('gradebook/', views.gradebook, name='gradebook'),
    path('gradebook/<int:class_id>/', views.class_gradebook, name='class_gradebook'),
    path('gradebook/<int:class_id>/subjects/', views.class_subjects, name='class_subjects'),
    path('gradebook/<int:class_id>/teachers/', views.class_teachers, name='class_teachers'),
    path('gradebook/<int:class_id>/grades/', views.class_grades, name='class_grades'),
    path('gradebook/<int:class_id>/attendance/', views.class_attendance, name='class_attendance'),
    path('gradebook/<int:class_id>/stats/', views.class_stats, name='class_stats'),
    path('gradebook/<int:class_id>/homework/', views.class_homework, name='class_homework'),
    path('gradebook/<int:class_id>/docs/', views.class_docs, name='class_docs'),
    path('gradebook/<int:class_id>/settings/', views.class_settings, name='class_settings'),
    path('gradebook/<int:class_id>/subject/<int:subject_id>/',views.subject_grades,name='subject_grades')
]
