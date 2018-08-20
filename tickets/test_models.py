from django.test import TestCase
from accounts.models import User
from .models import Ticket, TicketComment

class TestTicketModels(TestCase):
    def test_ticket(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        ticket = Ticket(requester=user, title='Test ticket', description='Ticket description')
        ticket.save()
        print('TestTicketModels: Ticket - test_ticket \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5} \n \
               Expected: {6}, Actual: {7}'.format('Test ticket', ticket.title,
                                                  'Ticket description', ticket.description,
                                                  'Bug', ticket.type,
                                                  'Logged', ticket.status))
        self.assertEqual(ticket.title, 'Test ticket')
        self.assertEqual(ticket.description, 'Ticket description')
        self.assertEqual(ticket.type, 'Bug')
        self.assertEqual(ticket.status, 'Logged')

    def test_ticket_comment(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        ticket = Ticket(requester=user, title='Test ticket', description='Ticket description')
        ticket.save()
        ticket_comment = TicketComment(author=user, ticket=ticket, comment='Test comment')
        ticket_comment.save()

        print('TestTicketModels: TicketComment - test_ticket_comment \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format('Test comment', ticket_comment.comment,
                                                  'test@test.com', ticket_comment.author.email))

        self.assertEqual(ticket_comment.author.email, 'test@test.com')
        self.assertEqual(ticket_comment.comment, 'Test comment')
