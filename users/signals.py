import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import LocalUser

@receiver(pre_save, sender=LocalUser)
def delete_old_profile_photo(sender, instance, **kwargs):
    # Если объект уже существует в базе данных
    if instance.pk:
        try:
            old_photo = LocalUser.objects.get(pk=instance.pk).photo
        except LocalUser.DoesNotExist:
            return

        new_photo = instance.photo

        # Удаляем старое фото, если загружено новое
        if old_photo and old_photo != new_photo:
            old_photo_path = os.path.join(settings.MEDIA_ROOT, old_photo.path)
            if os.path.isfile(old_photo_path):
                os.remove(old_photo_path)