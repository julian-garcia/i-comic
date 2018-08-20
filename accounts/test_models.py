from django.test import TestCase
from .models import User

class TestAccountsModels(TestCase):
    def test_new_user(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        print('TestAccountsModels: User - test_new_user \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5}'.format('test@test.com', user.email,
                                                  'Test', user.first_name,
                                                  'Case', user.last_name))

        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'Case')
