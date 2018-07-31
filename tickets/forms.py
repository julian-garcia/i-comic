from django import forms
from .models import Ticket, TicketComment

class TicketAddForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description','type','status']
