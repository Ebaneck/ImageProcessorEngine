
import os

from celery.decorators import task
from celery import shared_task

from PIL import Image, ImageDraw, ImageFont

from django.conf import settings
from .models import ImageProcessorModel
from imageProcessor.celery import app


@app.task
def add_waterMark(photo_id, selected_flag):
    try:
        photo = ImageProcessorModel.objects.get(id=photo_id)
    except ImageProcessorModel.DoesNotExist:
        photo = None

    if photo:
        image = Image.open(photo.photo.file)
        watermark_img_name = settings.STATIC_ROOT + "/rejected" + '.jpeg'
        if(selected_flag == "accepted"):
            watermark_img_name = settings.STATIC_ROOT + "/accepted" + '.jpeg'
        watermark = Image.open(watermark_img_name)
        image.paste(watermark, (0, 0), watermark.convert('RGBA'))
        image.save(str(settings.CUSTOM_PATH) + photo.photo.url, format="png")
        return "Task completed!!"

    return None


