from django.db import models
from django.contrib.auth.models import User

class ImgPlace(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to ='uploads/'),
    place = models.CharField(max_length=255, default='')
    image_url = models.URLField(max_length=200, default='')
    guess_by = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.place


class NamesPlace(models.Model):
    names = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.names
