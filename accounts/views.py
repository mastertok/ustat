from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied

from .models import Profile, Education, WorkExperience, Achievement, User
from .forms import (
    ProfileForm, EducationForm,
    WorkExperienceForm, AchievementForm, ProfileSettingsForm
)
from courses.models import Course

class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        if profile.user.role == 'teacher':
            # Получаем параметры фильтрации из GET-запроса
            category = self.request.GET.get('category')
            price_order = self.request.GET.get('price')
            popularity = self.request.GET.get('popularity')
            
            # Базовый QuerySet курсов учителя
            courses = Course.objects.filter(teacher=profile.user, status='published')
            
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
            context['total_students'] = courses.aggregate(total=Count('enrolled_students'))['total'] or 0
            context['total_courses'] = courses.count()
            context['published_courses'] = courses.filter(status='published').count()
            context['total_reviews'] = courses.aggregate(total=Count('reviews'))['total'] or 0
            context['courses'] = courses
            
            # Категории для фильтра
            context['categories'] = Course.objects.filter(teacher=profile.user).values(
                'category__name', 'category__slug'
            ).distinct()
        
        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = request.user.profile
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
            experience.profile = request.user.profile
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
            achievement.profile = request.user.profile
            achievement.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def delete_education(request, pk):
    education = get_object_or_404(Education, pk=pk, profile=request.user.profile)
    education.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_work_experience(request, pk):
    experience = get_object_or_404(WorkExperience, pk=pk, profile=request.user.profile)
    experience.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_achievement(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk, profile=request.user.profile)
    achievement.delete()
    return JsonResponse({'status': 'success'})

def teacher_profile(request, custom_url):
    """Отображает профиль преподавателя"""
    profile = get_object_or_404(Profile, custom_url=custom_url, user__role='teacher')
    context = {
        'profile': profile,
        'courses_count': Course.objects.filter(user_roles__user=profile.user, user_roles__role='teacher').count()
    }
    return render(request, 'accounts/teacher_profile.html', context)

def teacher_courses(request, custom_url):
    """Отображает список курсов преподавателя"""
    profile = get_object_or_404(Profile, custom_url=custom_url, user__role='teacher')
    courses = Course.objects.filter(
        user_roles__user=profile.user,
        user_roles__role='teacher'
    ).order_by('-created_at')
    
    context = {
        'profile': profile,
        'courses': courses
    }
    return render(request, 'accounts/teacher_courses.html', context)

@login_required
def profile_settings(request):
    """Настройки профиля пользователя"""
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        # Обработка формы обновления профиля
        form = ProfileSettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Проверяем custom_url если пользователь - преподаватель
            if request.user.role == 'teacher' and 'custom_url' in form.changed_data:
                custom_url = form.cleaned_data['custom_url']
                if Profile.objects.filter(custom_url=custom_url).exclude(id=profile.id).exists():
                    form.add_error('custom_url', 'Этот URL уже занят')
                    return render(request, 'accounts/profile_settings.html', {'form': form})
            
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile_settings')
    else:
        form = ProfileSettingsForm(instance=profile)
    
    return render(request, 'accounts/profile_settings.html', {'form': form})
