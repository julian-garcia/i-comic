from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketAddForm
from .models import Ticket, TicketComment

def ticket_listing(request):
    tickets = Ticket.objects.all()

    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    ticket_list = paginator.get_page(page)

    return render(request, 'tickets.html', {'ticket_list': ticket_list})
