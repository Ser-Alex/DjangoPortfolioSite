import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


class HistoryWedding(models.Model):
    title = models.CharField(max_length=50, null=False)
    intro = models.TextField(max_length=500, null=False)
    preview = models.ImageField(upload_to='image/%y/%m/%d/', null=False)
    preview_small = models.ImageField( null=True, blank=True)
    active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        if self.preview and os.path.isfile(self.preview.path):
            os.remove(self.preview.path)
        if self.preview_small and os.path.isfile(self.preview_small.path):
            os.remove(self.preview_small.path)

        super(HistoryWedding, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.preview:
            img = Image.open(self.preview.path)

            if img.height > 360 or img.width > 360:
                output_size = (360, 720)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                thumb_io = BytesIO()
                img.save(thumb_io, img.format, quality=85)

                file_name = self.preview.name
                self.preview_small.save(file_name, ContentFile(thumb_io.getvalue()), save=False)

        super().save(*args, **kwargs)