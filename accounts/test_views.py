from django.shortcuts import reverse
from django.test import TestCase

class TestAccountsViews(TestCase):
    def test_login_page(self):
        '''
        Verify that the login view applies the correct template and returns a web page to the browser
        '''
        page = self.client.get(reverse('login'))
        print('TestAccountsViews: login - test_login_page \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, page.status_code,
                                                  'login.html', page))

        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")

    def test_register_page(self):
        '''
        Verify that the register view applies the correct template and returns a web page to the browser
        '''
        page = self.client.get(reverse('register'))
        print('TestAccountsViews: register - test_register_page \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, page.status_code,
                                                  'register.html', page))

        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "register.html")
