from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from .forms import TicketAddForm, TicketEditForm
from .models import Ticket, TicketComment

def ticket_listing(request):
    tickets = Ticket.objects.all()

    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    ticket_list = paginator.get_page(page)

    return render(request, 'tickets.html', {'ticket_list': ticket_list})

def ticket_view(request, id):
    ticket = Ticket.objects.get(pk=id)
    comments = TicketComment.objects.all().filter(ticket=ticket)

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    ticket_comments = paginator.get_page(page)

    return render(request, 'ticket.html',
                  {'ticket': ticket, 'ticket_comments': ticket_comments})

@login_required
def ticket_add(request):
    if request.method == 'POST':
        ticket_form = TicketAddForm(request.POST)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect(reverse('ticket_listing'))
    else:
        ticket_form = TicketAddForm()

    return render(request, 'ticket_add.html', {'ticket_form': ticket_form})

@login_required
def ticket_edit(request, id):
    ticket = Ticket.objects.get(pk=id)

    if request.method == 'POST':
        ticket_form = TicketEditForm(request.POST or None, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect(reverse('ticket_view', args=[id]))
    else:
        ticket_form = TicketEditForm(instance=ticket)

    return render(request, 'ticket_edit.html', {'ticket_form': ticket_form, 'ticket': ticket})

@login_required
def ticket_upvote(request, id):
    ticket = Ticket.objects.get(pk=id)
    if ticket.upvotes is None:
        ticket.upvotes = 0
    ticket.upvotes += 1
    ticket.save()
    print(ticket.upvotes)
    return redirect(reverse('ticket_view', args=[id]))
