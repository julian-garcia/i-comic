import datetime, random
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketAddForm, TicketEditForm, TicketCommentAddForm
from .models import Ticket, TicketComment, TicketUpvoter
from .tickets import register_upvote, create_ticket

def ticket_listing(request):
    '''
    Paginated listing of all tickets raised by users. Tickets are either
    feature requests or bug reports
    '''
    # There are two tabs - one for tickets being worked on and another for completed tickets.
    # Splitting the data that way simplifies the logic required within the template.
    tickets = Ticket.objects.all().filter(~Q(status='Completed') & ~Q(status='Cancelled')).order_by('-upvotes', '-date_raised', 'title')
    ctickets = Ticket.objects.all().filter(Q(status='Completed') | Q(status='Cancelled')).order_by('-upvotes', '-date_raised', 'title')

    paginator = Paginator(tickets, 5)
    page = request.GET.get('page')
    ticket_list = paginator.get_page(page)

    paginator = Paginator(ctickets, 5)
    page = request.GET.get('page')
    completed_ticket_list = paginator.get_page(page)

    return render(request, 'tickets.html',
                  {'ticket_list': ticket_list,
                   'completed_ticket_list': completed_ticket_list})

def ticket_view(request, id):
    '''
    Single tiket view - from here the user can: view ticket details (title, description,
    developer response), they can also make comments and upvote a ticket to raise its priority
    '''
    ticket = Ticket.objects.get(pk=id)
    comments = TicketComment.objects.all().filter(ticket=ticket).order_by('-date_comment')

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    ticket_comments = paginator.get_page(page)

    return render(request, 'ticket.html',
                  {'ticket': ticket, 'ticket_comments': ticket_comments})

@login_required
def ticket_add(request):
    '''
    There are two branches for adding a ticket:
    Bug - this is free so the ticket is simply saved in the backend
    Feature - this paid for so the ticket is first added to a shopping cart
              and will only be committed upon payment in the checkout app
    '''
    if request.method == 'POST':
        ticket_form = TicketAddForm(request.POST)

        if ticket_form.is_valid():
            # Save the ticket in the backend if this is a bug or add 
            # it to the shopping cart if it's a feature that needs paying for 
            create_ticket(request, ticket_form)
            return redirect(reverse('ticket_listing'))
    else:
        ticket_form = TicketAddForm()

    return render(request, 'ticket_add.html', {'ticket_form': ticket_form})

@login_required
def ticket_edit(request, id):
    '''
    Ticket editing is meant for developers only so they are able to update the status
    and enter some text to advise users of the current state of play in more detail
    '''
    ticket = Ticket.objects.get(pk=id)

    if request.user.is_staff:
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
    '''
    Upvoting allows users to push bugs or features to the top of the list so that developers
    address them sooner. Bugs are upvoted for free so the increment is applied and committed.
    Feature upvotes are paid for so they need to be directed to a session based shopping cart
    before flowing through to the backend upon payment - the checkout app handles this.
    '''
    ticket = Ticket.objects.get(pk=id)
    upvotes = TicketUpvoter.objects.all().filter(upvoter_ticket=ticket,
                                                 upvoter_user=request.user)

    if not upvotes:
        # Save the upvote if the ticket is a bug or add it to the cart if it's a new feature
        register_upvote(request, ticket)
    else:
        messages.info(request, 'You have already upvoted this.')
        return redirect(reverse('ticket_view', args=[id]))

    return redirect(reverse('ticket_view', args=[id]))

@login_required
def comment_add(request, id):
    '''
    Tickets can have an unlimited number of comments to facilitate user discussion.
    '''
    ticket = Ticket.objects.get(pk=id)

    if request.method == 'POST':
        comment_form = TicketCommentAddForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.ticket = ticket
            comment.save()

        return redirect(reverse('ticket_view', args=[id]))
    else:
        comment_form = TicketCommentAddForm()

    return render(request, 'comment_add.html', {'comment_form': comment_form, 'ticket': ticket})

def update_tickets(request):
    '''
    This view is used purely for randomising the artificially generated data
    created using django-autofixture
    '''
    tickets = Ticket.objects.all()

    for ticket in tickets:
        new_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1,365))
        new_savedate = new_date + datetime.timedelta(days=random.randint(1,30))
        typeno = random.randint(1,2)
        if typeno == 1:
            new_type = 'Bug'
        else:
            new_type = 'Feature'

        statusno = random.randint(1,6)
        if statusno == 1:
            new_status = 'Logged'
        elif statusno == 2:
            new_status = 'Started'
        elif statusno == 3:
            new_status = 'In progress'
        elif statusno == 4:
            new_status = 'On hold'
        elif statusno == 5:
            new_status = 'Completed'
        elif statusno == 6:
            new_status = 'Cancelled'
        else:
            new_status = 'Logged'

        Ticket.objects.filter(pk=ticket.id).update(date_raised=new_date)
        Ticket.objects.filter(pk=ticket.id).update(date_last_saved=new_savedate)
        Ticket.objects.filter(pk=ticket.id).update(type=new_type)
        Ticket.objects.filter(pk=ticket.id).update(status=new_status)
        Ticket.objects.filter(pk=ticket.id).update(upvotes=random.randint(0,20))

    return redirect(reverse('ticket_listing'))
