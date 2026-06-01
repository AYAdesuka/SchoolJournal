from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('registration/', views.register_view, name='registration'),
    path('profile/', views.my_profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='main:home'), name='logout'),
]