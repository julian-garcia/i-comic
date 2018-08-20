from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from django.conf import settings
from importlib import import_module
from accounts.models import User
from .views import checkout

class TestCheckoutView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {'email': 'user@test.com', 'password': 'Secret12'}
        self.user = User.objects.create_user(**self.credentials)
        # Need to establish a session environment for testing
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store

    def test_checkout_calc(self):
        request = self.factory.get(reverse('checkout'))
        request.user = self.user
        request.session = self.session

        cart = []
        cart.append({'title': 'test title',
                     'description': 'test desc',
                     'feature_cost': 4.35})
        cart.append({'title': 'test title2',
                     'description': 'test desc2',
                     'feature_cost': 3.7})
        request.session['cart'] = cart

        response = checkout(request)
        cart_total = response.content.find(b'8.05')

        print('TestCheckoutView: checkout - test_checkout_calc \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format('Response code: 200', response.status_code,
                                                  'Total: 8.05', response.content[cart_total:cart_total+4]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'8.05' in response.content)
