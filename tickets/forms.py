from django import forms
from .models import Ticket, TicketComment

class TicketAddForm(forms.ModelForm):
    feature_cost = forms.DecimalField(min_value=1.0, label='Feature cost <i class="fas fa-pound-sign"></i>')
    class Meta:
        model = Ticket
        fields = ['title', 'type', 'description', 'feature_cost']

class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'solution']

class TicketCommentAddForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment']
