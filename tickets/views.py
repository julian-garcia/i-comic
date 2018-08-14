from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketAddForm, TicketEditForm, TicketCommentAddForm
from .models import Ticket, TicketComment, TicketUpvoter

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
            if ticket_form.cleaned_data.get('type') == 'Bug':
                ticket = ticket_form.save(commit=False)
                ticket.requester = request.user
                ticket.save()
            elif ticket_form.cleaned_data.get('feature_cost') is not None and ticket_form.cleaned_data.get('feature_cost') > 0:
                # Add ticket to cart with manually entered price
                cart = request.session.get('cart', [])
                cart.append({'title': ticket_form.cleaned_data.get('title'),
                             'description': ticket_form.cleaned_data.get('description'),
                             'feature_cost': str(ticket_form.cleaned_data.get('feature_cost'))})
                request.session['cart'] = cart
                messages.info(request, 'A new feature has been added to your cart.')
            else:
                messages.error(request, 'The cost for a new feature must be above zero.')

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
    # Each user upvote is saved in the database to ensure that we only register
    # one upvote per user. Here we check that the user has not already upvoted this ticket.
    # If they have, the upvote is skipped and a relevant message passed back to the user
    if not upvotes:
        if ticket.type == 'Bug':
            if ticket.upvotes is None:
                ticket.upvotes = 0
            ticket.upvotes += 1
            ticket.save()
            upvoter = TicketUpvoter(upvoter_ticket=ticket, upvoter_user=request.user)
            upvoter.save()
        else:
            # Add upvoted feature to the upvote cart
            cart_upvotes = request.session.get('cart_upvotes', [])
            # Check that an upvote has not alread been added to the cart to prevent multiple upvotes
            if not any(d['id'] == ticket.id for d in cart_upvotes):
                cart_upvotes.append({'id': ticket.id, 'title': ticket.title, 'cost': 1})
                request.session['cart_upvotes'] = cart_upvotes
                messages.info(request, 'An upvote for this feature has been added to your cart.')
            else:
                messages.info(request, 'An upvote for this feature is already in your cart.')
            return redirect(reverse('ticket_view', args=[id]))
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
