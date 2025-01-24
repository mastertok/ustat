from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    # API для управления образованием
    path('education/add/', views.add_education, name='add_education'),
    path('education/<int:pk>/delete/', views.delete_education, name='delete_education'),
    
    # API для управления опытом работы
    path('experience/add/', views.add_work_experience, name='add_work_experience'),
    path('experience/<int:pk>/delete/', views.delete_work_experience, name='delete_work_experience'),
    
    # API для управления достижениями
    path('achievement/add/', views.add_achievement, name='add_achievement'),
    path('achievement/<int:pk>/delete/', views.delete_achievement, name='delete_achievement'),
]
