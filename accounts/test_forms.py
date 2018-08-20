from django.test import TestCase
from .models import User
from .forms import UserLoginForm, UserRegistrationForm

class TestAccountsForms(TestCase):
    def test_user_login(self):
        form = UserLoginForm({'email':'test@test.com', 'password':'xyz'})
        print('TestAccountsForms: UserLoginForm - test_user_login \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format('Email input element', form['email'],
                                                  'Password input element', form['password']))
        self.assertTrue(form.is_valid())

    def test_user_registration(self):
        form = UserRegistrationForm({'email':'test@test.com', 'first_name':'Test', 'last_name':'Case', 'password1':'ABxyz123', 'password2':'ABxyz123'})
        print('TestAccountsForms: UserRegistrationForm - test_user_registration \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5} \n \
               Expected: {6}, Actual: {7} \n \
               Expected: {8}, Actual: {9}'.format('Email input element', form['email'],
                                                  'Forename input element', form['first_name'],
                                                  'Surname input element', form['last_name'],
                                                  'Password1 input element', form['password1'],
                                                  'Password2 input element', form['password2']))
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        form = UserLoginForm({'email': ""})
        print('TestAccountsForms: UserLoginForm - test_missing_email \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format('Email input element no value', form['email'],
                                                  'Password input element', form['password']))

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])
