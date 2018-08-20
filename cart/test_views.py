from django.shortcuts import reverse
from django.test import TestCase
from accounts.models import User
from .views import view_cart, adjust_cart

class TestCartViews(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'user@test.com',
            'password': 'Secret12'}
        User.objects.create_user(**self.credentials)

    def test_cart_page(self):
        '''
        Verify that the view_cart view applies the login template with a subsequent redirect
        to the cart
        '''
        page = self.client.get(reverse('view_cart'))
        print('TestCartViews: view_cart - test_cart_page \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(302, page.status_code,
                                                  'login url redirect', page))

        self.assertEqual(page.status_code, 302)
        self.assertTemplateNotUsed(page, "cart.html")

    def test_cart_total(self):
        '''
        Check that the correct total is calculated for all items in the cart
        '''
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

        cart = []
        cart.append({'title': 'test',
                     'description': 'description',
                     'feature_cost': str(2.30)})
        response.context['request'].session['cart'] = cart

        cart_upvotes = []
        cart_upvotes.append({'id': 1, 'title': 'test title', 'cost': 1})
        response.context['request'].session['cart_upvotes'] = cart_upvotes

        page = view_cart(response.context['request'])
        cart_total = page.content.find(b'3.30')

        print('TestCartViews: view_cart - test_cart_total \n \
               Expected: {0}, Actual: {1}'.format(3.3, page.content[cart_total:cart_total+4]))

        self.assertTrue(b'3.30' in page.content)
