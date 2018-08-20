from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from accounts.models import User
from .views import comic_strip_listing, comic_strip, comic_strip_add
from .models import ComicStrip

class TestComicStripViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {'email': 'user@test.com', 'password': 'Secret12'}
        self.user = User.objects.create_user(**self.credentials)

    def test_comic_strip_listing(self):
        '''
        Verify that the comic strip listing is rendered as the home page
        '''
        request = self.factory.get(reverse('index'))
        request.user= self.user

        response = comic_strip_listing(request)
        print('TestComicStripViews: comic_strip_listing - test_comic_strip_listing \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/")

    def test_comic_strip(self):
        '''
        Single comic strip view displays the comic strip under the expected URL
        '''
        strip = ComicStrip(title='Strip title', description='Strip desc', author=self.user)
        strip.save()

        request = self.factory.get(reverse('comic_strip', args=[strip.id]))
        request.user = self.user

        response = comic_strip(request, strip.id)
        print('TestComicStripViews: comic_strip - test_comic_strip \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/comic-strip/view/{0}'.format(strip.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/comic-strip/view/{0}'.format(strip.id))

    def test_comic_strip_add(self):
        '''
        Add a comic strip view displays the form at the expected URL
        '''
        request = self.factory.get(reverse('comic_strip_add'))
        request.user = self.user

        response = comic_strip_add(request)
        print('TestComicStripViews: comic_strip_add - test_comic_strip_add \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/comic-strip/add', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/comic-strip/add')

    def test_comic_strip_frame_add(self):
        '''
        Single comic strip view displays the comic strip under the expected URL
        '''
        strip = ComicStrip(title='Strip title', description='Strip desc', author=self.user)
        strip.save()

        request = self.factory.get(reverse('comic_strip_frame_add', args=[strip.id]))
        request.user = self.user

        response = comic_strip(request, strip.id)
        print('TestComicStripViews: comic_strip_frame_add - test_comic_strip_frame_add \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/comic-strip/add-frame/{0}'.format(strip.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/comic-strip/add-frame/{0}'.format(strip.id))
