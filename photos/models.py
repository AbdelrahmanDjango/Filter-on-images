from io import BytesIO
from uuid import uuid4
from django.db import models
from django.core.files.base import ContentFile
from .utils import get_filter_image
import PIL
from PIL import Image
import numpy as np


class Photos(models.Model):
    Actions = [
        ('NO_FILTER', 'no_filter'),
        ('COLORIZED', 'colorized'),
        ('GRAYSCALE', 'grayscale'),
        ('BLURRED', 'blurred'),
    ]
    image = models.ImageField(upload_to='images')
    action = models.CharField(max_length=50, choices=Actions)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs):
        pil_img = Image.open(self.image)
        cv_img = np.array(pil_img)
        img = get_filter_image(cv_img, self.action)
        im_pil = Image.fromarray(img)
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        filename = f"{uuid4()}.png"
        self.image.save(filename, ContentFile(image_png), save=False)
        super().save(*args, **kwargs)