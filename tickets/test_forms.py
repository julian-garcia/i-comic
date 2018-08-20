from django.test import TestCase
from .forms import TicketAddForm, TicketCommentAddForm

class TestTicketForms(TestCase):
    def test_ticket_add_form(self):
        form = TicketAddForm({'title': 'Test title', 'type': 'Bug', 'description': 'Test description', 'feature_cost': 1.5})
        print('TestTicketForms: TicketAddForm - test_ticket_add_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())

    def test_ticket_comment_form(self):
        form = TicketCommentAddForm({'comment':'my comment'})
        print('TestTicketForms: TicketCommentAddForm - test_ticket_comment_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())
