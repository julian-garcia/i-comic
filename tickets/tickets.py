from .models import TicketUpvoter
from django.shortcuts import redirect, reverse
from django.contrib import messages

def register_upvote(request, ticket):
    '''
    Each user upvote is saved in the database to ensure that we only register
    one upvote per user. Here we check that the user has not already upvoted this ticket.
    If they have, the upvote is skipped and a relevant message passed back to the user
    '''
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

def create_ticket(request, ticket_form):
    '''
    Save the ticket in the backend database if the ticket is a bug,
    otherwise save the ticket in the shopping cart as the user will
    need to pay before the ticket is committed to the backend
    '''
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

def listing():
    pass