from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('<str:custom_url>/', views.teacher_profile, name='profile'),
    path('<str:custom_url>/courses/', views.teacher_courses, name='courses'),
]
