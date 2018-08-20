from django.test import TestCase
from accounts.models import User
from .models import ComicStrip, ComicStripFrame

class TestComicStripModels(TestCase):
    def test_comic_strip(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        comic_strip = ComicStrip(title='Test', description='Desc', author=user)
        comic_strip.save()
        print('TestComicStripModels: ComicStrip - test_comic_strip \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5}'.format('Test', comic_strip.title,
                                                  'Desc', comic_strip.description,
                                                  'test@test.com', comic_strip.author.email))
        self.assertEqual(comic_strip.title, 'Test')
        self.assertEqual(comic_strip.description, 'Desc')
        self.assertEqual(comic_strip.author.email, 'test@test.com')

    def test_comic_strip_frame(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        comic_strip = ComicStrip(title='Test', description='Desc', author=user)
        comic_strip.save()
        frame = ComicStripFrame(comic_strip=comic_strip, narrative='blah', sequence=1)
        frame.save()

        print('TestComicStripModels: ComicStripFrame - test_comic_strip_frame \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5}'.format('Test', frame.comic_strip.title,
                                                  'blah', frame.narrative,
                                                  1, frame.sequence))

        self.assertEqual(frame.comic_strip.title, 'Test')
        self.assertEqual(frame.narrative, 'blah')
        self.assertEqual(frame.sequence, 1)
