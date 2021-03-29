from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.

# callable storage use
# def select_storage():
#     return MyLocalStorage() if settings.DEBUG else MyRemoteStorage()

# Mount a persistent volume for the django backend to persist uploaded images
# In a production usecase, use a file storage backend with s3 capabilities

# fs = FileSystemStorage(location='/Users/ebaneck/Desktop/photos')

class ImageProcessorModel(models.Model):
    # photo = models.ImageField(storage=fs)
    photo = models.ImageField()
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    image_verified = models.BooleanField(default=False)
    image_rejected = models.BooleanField(null=True, default=None)
