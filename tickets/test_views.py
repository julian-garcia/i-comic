from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from accounts.models import User
from .views import comment_add, ticket_add, ticket_edit, ticket_listing, ticket_upvote, ticket_view
from .models import Ticket, TicketComment, TicketUpvoter

class TestTicketViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {'email': 'user@test.com', 'password': 'Secret12', 'is_staff': True}
        self.user = User.objects.create_user(**self.credentials)

    def test_ticket_listing(self):
        '''
        Verify that the ticket listing is rendered at the correct url
        '''
        request = self.factory.get(reverse('ticket_listing'))
        request.user = self.user

        response = ticket_listing(request)
        print('TestTicketViews: ticket_listing - test_ticket_listing \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'tickets', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/tickets/")

    def test_ticket_add(self):
        '''
        Verify that the ticket add form is rendered at the correct url
        '''
        request = self.factory.get(reverse('ticket_add'))
        request.user = self.user

        response = ticket_add(request)
        print('TestTicketViews: ticket_add - test_ticket_add \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'tickets/add', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/tickets/add")

    def test_ticket_view(self):
        '''
        Verify that the single ticket view is rendered at the correct url
        '''
        ticket = Ticket(requester=self.user, title='Test ticket', description='Ticket description')
        ticket.save()
        request = self.factory.get(reverse('ticket_view', args=[ticket.id]))
        request.user = self.user

        response = ticket_view(request, ticket.id)
        print('TestTicketViews: ticket_view - test_ticket_view \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'tickets/view/{0}'.format(ticket.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/tickets/view/{0}".format(ticket.id))

    def test_ticket_edit(self):
        '''
        Verify that the single ticket edit form is rendered at the correct url
        '''
        ticket = Ticket(requester=self.user, title='Test ticket', description='Ticket description')
        ticket.save()
        request = self.factory.get(reverse('ticket_edit', args=[ticket.id]))
        request.user = self.user

        response = ticket_edit(request, ticket.id)
        print('TestTicketViews: ticket_edit - test_ticket_edit \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'tickets/edit/{0}'.format(ticket.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/tickets/edit/{0}".format(ticket.id))

    def test_comment_add(self):
        '''
        Verify that the comment addition form for a single ticket is rendered at the correct url
        '''
        ticket = Ticket(requester=self.user, title='Test ticket', description='Ticket description')
        ticket.save()
        request = self.factory.get(reverse('comment_add', args=[ticket.id]))
        request.user = self.user

        response = comment_add(request, ticket.id)
        print('TestTicketViews: comment_add - test_comment_add \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'tickets/comment/{0}'.format(ticket.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/tickets/comment/{0}".format(ticket.id))

    def test_ticket_upvote(self):
        '''
        Verify that single ticket upvotes are rendered at the correct url
        '''
        ticket = Ticket(requester=self.user, title='Test ticket', description='Ticket description')
        ticket.save()
        request = self.factory.get(reverse('ticket_upvote', args=[ticket.id]))
        request.user = self.user

        response = ticket_upvote(request, ticket.id)
        print('TestTicketViews: ticket_upvote - test_ticket_upvote \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(302, response.status_code,
                                                  'tickets/upvote/{0}'.format(ticket.id), request.path))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.path, "/tickets/upvote/{0}".format(ticket.id))
