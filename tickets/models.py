from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('Bug','Bug'),
        ('Feature','Feature'),
    )
    TICKET_STATUS_CHOICES = (
        ('Logged','Logged'),
        ('Started','Started'),
        ('In progress','In progress'),
        ('On hold','On hold'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    solution = models.TextField('Solution / Proposed solution', null=True, blank=True)
    date_raised = models.DateTimeField(auto_now_add=True)
    date_last_saved = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10,choices=TICKET_TYPE_CHOICES, default='Bug')
    status = models.CharField(max_length=12,choices=TICKET_STATUS_CHOICES, default='Logged')
    upvotes = models.IntegerField(null=True, blank=True)
    feature_cost = models.DecimalField("Contribution towards feature development", max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{0}-{1}'.format(self.title, self.requester)

class TicketComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date_comment = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return '{0}-{1}'.format(self.ticket, self.comment)
