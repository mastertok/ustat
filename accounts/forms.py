from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, Education, WorkExperience, Achievement

User = get_user_model()

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    bio = forms.CharField(widget=forms.Textarea, label='О себе')
    avatar = forms.ImageField(required=False, label='Фото профиля')

    class Meta:
        model = Profile
        fields = [
            'social_links', 'language'
        ]
        widgets = {
            'social_links': forms.Textarea(attrs={'placeholder': '{"vk": "https://vk.com/...", "telegram": "@username"}'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone
            self.fields['bio'].initial = self.instance.bio
            
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Сохраняем данные пользователя
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            if self.cleaned_data['avatar']:
                profile.avatar = self.cleaned_data['avatar']
            profile.bio = self.cleaned_data['bio']
            user.save()
            profile.save()
            self.save_m2m()  # Сохраняем many-to-many поля
        return profile

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfileSettingsForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    password1 = forms.CharField(widget=forms.PasswordInput, required=False, label='Новый пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['email'].initial = self.instance.email
            self.fields['phone'].initial = self.instance.phone

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            
            if self.cleaned_data['password1']:
                user.set_password(self.cleaned_data['password1'])
            
            user.save()
        return user
