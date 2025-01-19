from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from .models import TeacherProfile, Education, WorkExperience, Achievement
from .forms import (
    TeacherProfileForm, EducationForm,
    WorkExperienceForm, AchievementForm
)
from courses.models import Course

class TeacherProfileView(DetailView):
    model = TeacherProfile
    template_name = 'accounts/teacher_profile.html'
    context_object_name = 'teacher'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.get_object()
        
        # Получаем параметры фильтрации из GET-запроса
        category = self.request.GET.get('category')
        price_order = self.request.GET.get('price')
        popularity = self.request.GET.get('popularity')
        
        # Базовый QuerySet курсов учителя
        courses = Course.objects.filter(teacher=teacher, status='published')
        
        # Применяем фильтры
        if category:
            courses = courses.filter(category__slug=category)
        
        # Сортировка по цене
        if price_order == 'asc':
            courses = courses.order_by('price')
        elif price_order == 'desc':
            courses = courses.order_by('-price')
            
        # Сортировка по популярности
        if popularity == 'rating':
            courses = courses.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        elif popularity == 'students':
            courses = courses.annotate(total_students=Count('enrolled_students')).order_by('-total_students')
        
        # Статистика
        context['total_students'] = teacher.students_count
        context['total_courses'] = teacher.total_courses()
        context['published_courses'] = teacher.published_courses()
        context['total_reviews'] = teacher.reviews_count
        context['courses'] = courses
        
        # Категории для фильтра
        context['categories'] = Course.objects.filter(teacher=teacher).values(
            'category__name', 'category__slug'
        ).distinct()
        
        return context

class TeacherProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherProfileForm
    template_name = 'accounts/teacher_profile_edit.html'
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
    def get_object(self, queryset=None):
        return get_object_or_404(TeacherProfile, user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('teacher_profile', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.teacher = request.user.teacher_profile
            education.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def add_work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.teacher = request.user.teacher_profile
            experience.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def add_achievement(request):
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.teacher = request.user.teacher_profile
            achievement.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def delete_education(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if education.teacher.user != request.user:
        raise PermissionDenied
    education.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_work_experience(request, pk):
    experience = get_object_or_404(WorkExperience, pk=pk)
    if experience.teacher.user != request.user:
        raise PermissionDenied
    experience.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_achievement(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    if achievement.teacher.user != request.user:
        raise PermissionDenied
    achievement.delete()
    return JsonResponse({'status': 'success'})

def create_teacher_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль учителя при регистрации"""
    if created and instance.role == 'teacher':
        TeacherProfile.objects.create(
            user=instance,
            slug=instance.username
        )
