from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('gradebook/', views.gradebook, name='gradebook'),
    path('gradebook/<int:class_id>/', views.class_gradebook, name='class_gradebook'),
    path('gradebook/update/', views.update_grade, name='update_grade'),
]
