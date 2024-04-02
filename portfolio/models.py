from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify


class HistoryWedding(models.Model):
    # Модель историй
    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=60, verbose_name="Ссылка")
    intro = models.TextField(max_length=500, null=False, verbose_name='Основной текст')
    preview = models.ImageField(upload_to='image/%y/%m/%d/', null=False, verbose_name='Основное изображение')
    preview_small = models.ImageField(null=True, blank=True, verbose_name='Маленькое изображение')
    active = models.BooleanField(default=True, verbose_name='Активно')

    def save(self, *args, **kwargs):
        # Функция для сохранения маленькой фотографии и создания ссылки из названия
        super().save(*args, **kwargs)
        if self.preview and not self.preview_small:
            img = Image.open(self.preview.path)

            if img.height > 360 or img.width > 360:
                output_size = (360, 720)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                thumb_io = BytesIO()
                img.save(thumb_io, img.format, quality=85)

                file_name = self.preview.name
                self.preview_small.save(file_name, ContentFile(thumb_io.getvalue()), save=False)

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Историю'
        verbose_name_plural = 'Истории'


class HistoryImage(models.Model):
    history = models.ForeignKey('HistoryWedding', on_delete=models.CASCADE,
                                    related_name='images', verbose_name='Истории')
    image = models.ImageField(upload_to='image/%y/%m/%d/', null=False, verbose_name='Изображения')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
