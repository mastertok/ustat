from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import User, TeacherProfile

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает профиль учителя при регистрации пользователя с ролью 'teacher'
    """
    if created and instance.role == 'teacher':
        TeacherProfile.objects.create(
            user=instance,
            slug=slugify(instance.get_full_name() or instance.username)
        )
