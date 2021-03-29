from django.test import TestCase
from django.conf import settings
from imageProcessorApp.models import ImageProcessorModel

class ModelsTestCase(TestCase):
    def test_insert_image(self):
        """New images are uploaded correctly when saving"""
        img = settings.STATIC_ROOT + "/rejected" + '.jpeg'
        info = ImageProcessorModel(photo=img, image_verified=True, image_rejected=False)
        self.assertEqual(info.photo, img)
        self.assertEqual(info.image_verified, True)
        self.assertEqual(info.image_rejected, False)