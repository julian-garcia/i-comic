from tickets.models import Ticket, TicketUpvoter
from .models import OrderTransaction, Order
from django.conf import settings
from django.contrib import messages

import stripe
stripe.api_key = settings.STRIPE_SECRET

def process_payment(request, total, payment_form):
    '''
    Process the payment using the Stripe API, feeding back any error messages
    to this site if unsuccessful
    '''
    try:
        process_payment.charge_customer = stripe.Charge.create(
                             amount = int(total*100),
                             currency = 'gbp',
                             description = request.user.email,
                             card = payment_form.cleaned_data['stripe_id'],
                          )
    except stripe.error.CardError:
        messages.error(request, 'Your card was declined')

def commit_data(request, order_form, cart, cart_upvotes):
    '''
    Save the order, features and feature upvotes in the backend database
    '''
    order = order_form.save(commit=False)
    order.save()

    for item in cart:
        ticket = Ticket(title=item['title'],
                        type='Feature',
                        description=item['description'],
                        requester=request.user)
        ticket.save()
        order_transaction = OrderTransaction(
            order = order,
            ticket = ticket,
            cost = item['feature_cost']
            )
        order_transaction.save()

    for item in cart_upvotes:
        ticket = Ticket.objects.get(pk=item['id'])
        if ticket.upvotes is None:
            ticket.upvotes = 0
        ticket.upvotes += 1
        ticket.save()
        upvoter = TicketUpvoter(upvoter_ticket=ticket, upvoter_user=request.user)
        upvoter.save()
