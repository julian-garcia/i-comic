from django.test import TestCase
from tickets.models import Ticket
from accounts.models import User
from .models import Order, OrderTransaction

class TestCheckoutModels(TestCase):
    def test_order(self):
        order = Order(full_name='Test', phone_number='012345', country='gb', postcode='ab123')
        order.save()
        print('TestCheckoutModels: Order - test_order \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5} \n \
               Expected: {6}, Actual: {7}'.format('Test', order.full_name,
                                                  '012345', order.phone_number,
                                                  'gb', order.country,
                                                  'ab123', order.postcode))
        self.assertEqual(order.full_name, 'Test')
        self.assertEqual(order.phone_number, '012345')
        self.assertEqual(order.country, 'gb')
        self.assertEqual(order.postcode, 'ab123')

    def test_order_txn(self):
        order = Order(full_name='Test', phone_number='012345', country='gb', postcode='ab123')
        order.save()
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        ticket = Ticket(requester =user, title='Title')
        ticket.save()
        transaction = OrderTransaction(order=order, ticket=ticket, cost=2.2)
        transaction.save()

        print('TestCheckoutModels: OrderTransaction - test_order_txn \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5} \n \
               Expected: {6}, Actual: {7} \n \
               Expected: {8}, Actual: {9}'.format('Test', transaction.order.full_name,
                                                  '012345', transaction.order.phone_number,
                                                  user, transaction.ticket.requester,
                                                  'Title', transaction.ticket.title,
                                                  '2.2', transaction.cost))

        self.assertEqual(transaction.order.full_name, 'Test')
        self.assertEqual(transaction.order.phone_number, '012345')
        self.assertEqual(transaction.ticket.requester, user)
        self.assertEqual(transaction.ticket.title, 'Title')
        self.assertEqual(transaction.cost, 2.2)
