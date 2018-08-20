from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import ComicStripForm, ComicStripFrameAddForm
from django.conf import settings
import os

class TestComicStripForms(TestCase):
    def test_comic_strip_form(self):
        form = ComicStripForm({'title':'Test name','description':'0'})
        print('TestComicStripForms: ComicStripForm - test_comic_strip_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())

    def test_comic_strip_frame_form(self):
        mediafile = os.path.join(settings.BASE_DIR, 'media', 'images/484px-Trevor_under_moonlight.JPG')
        img = open(mediafile, 'rb')
        uploaded = SimpleUploadedFile(img.name, img.read())
        form = ComicStripFrameAddForm({'narrative':'1234'}, files={'image': uploaded})
        print('TestComicStripForms: ComicStripFrameAddForm - test_comic_strip_frame_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())
