import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import HistoryImage, HistoryWedding


@receiver(pre_delete, sender=HistoryImage)
def history_image_delete(sender, instance, **kwargs):
    # Сигнал удаления файла изображений
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_delete, sender=HistoryWedding)
def history_image_delete(sender, instance, **kwargs):
    # Сигнал удаления файла главного изображения и его маленькой копии
    if instance.preview and os.path.isfile(instance.preview.path):
        os.remove(instance.preview.path)
    if instance.preview_small and os.path.isfile(instance.preview_small.path):
        os.remove(instance.preview_small.path)