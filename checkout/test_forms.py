from django.test import TestCase
from .forms import OrderForm, PaymentForm

class TestCheckoutForms(TestCase):
    def test_order_form(self):
        form = OrderForm({'full_name':'Test name','phone_number':'0', 'street_address1':'abc',
                          'street_address2':'def', 'postcode':'ghi123', 'town_or_city':'town',
                          'county':'county', 'country':'uk'})
        print('TestCheckoutForms: OrderForm - test_order_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())

    def test_payment_form(self):
        form = PaymentForm({'credit_card_number':'1234','cvv':'110', 'expiry_month':'10',
                            'expiry_year':'2018','stripe_id':'0'})
        print('TestCheckoutForms: PaymentForm - test_payment_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())
