from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает профиль пользователя при регистрации
    """
    if created:
        Profile.objects.create(
            user=instance,
            slug=slugify(instance.get_full_name() or instance.username)
        )
