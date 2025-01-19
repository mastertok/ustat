from django import forms
from django.contrib.auth import get_user_model
from .models import TeacherProfile, Education, WorkExperience, Achievement

User = get_user_model()

class TeacherProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    bio = forms.CharField(widget=forms.Textarea, label='О себе')
    avatar = forms.ImageField(required=False, label='Фото профиля')

    class Meta:
        model = TeacherProfile
        fields = [
            'specializations', 'experience_summary', 'achievements_summary',
            'education_summary', 'social_links', 'teaching_style'
        ]
        widgets = {
            'social_links': forms.Textarea(attrs={'placeholder': '{"vk": "https://vk.com/...", "telegram": "@username"}'}),
            'teaching_style': forms.Textarea(attrs={'placeholder': 'Опишите ваш подход к обучению...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone
            self.fields['bio'].initial = self.instance.user.bio
            
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Сохраняем данные пользователя
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            user.bio = self.cleaned_data['bio']
            if self.cleaned_data['avatar']:
                user.avatar = self.cleaned_data['avatar']
            user.save()
            profile.save()
            self.save_m2m()  # Сохраняем many-to-many поля
        return profile

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['teacher']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['teacher']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ['teacher']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
        }
