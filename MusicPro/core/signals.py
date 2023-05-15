from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(user_logged_out)
def eliminar_usuario(sender, user, request, **kwargs):
    if not user.is_superuser:
        User.objects.filter(id=user.id).delete()