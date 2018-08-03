from django.contrib import admin
from .models import Ticket, TicketComment, TicketUpvoter

admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(TicketUpvoter)
