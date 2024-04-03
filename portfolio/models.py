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

    def __str__(self):
        return self.slug

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


class SiteSettings(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    image = models.ImageField(upload_to='image_main/')
    text_portfolio = models.TextField(verbose_name='Текст портфолио', max_length=400)
    text_about = models.TextField(verbose_name='Текст обо мне', max_length=400)
    text_contact = models.TextField(verbose_name='Текст контактов', max_length=400)
    link_contact = models.CharField(verbose_name='Ссылка контактов', max_length=100)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def __str__(self):
        return 'Нажми сюда, чтобы настроить!'

    class Meta:
        verbose_name = 'настройки сайта'
        verbose_name_plural = 'настройки сайта'


class Testimony(models.Model):
    text = models.TextField(verbose_name='Текст', max_length=400)
    author = models.CharField(verbose_name='Автор', max_length=100)

    class Meta:
        verbose_name = 'Высказывание'
        verbose_name_plural = 'Высказывания'