from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from tickets.models import Ticket, TicketUpvoter
from .models import OrderTransaction, Order
from .forms import OrderForm, PaymentForm
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
    cart_upvotes = request.session.get('cart_upvotes', [])
    cart = request.session.get('cart', [])
    total = sum(float(i['cost']) for i in cart_upvotes) + sum(float(i['feature_cost']) for i in cart)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        order_form = OrderForm(request.POST)
        if payment_form.is_valid() and order_form.is_valid():
            try:
                charge_customer = stripe.Charge.create(
                                     amount = int(total*100),
                                     currency = 'gbp',
                                     description = request.user.email,
                                     card = payment_form.cleaned_data['stripe_id'],
                                  )
            except stripe.error.CardError:
                messages.error(request, 'Your card was declined')

            if charge_customer.paid:
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

                request.session['cart'] = []
                request.session['cart_upvotes'] = []

                messages.info(request, 'Your payment was successful')
                return redirect(reverse('ticket_listing'))
            else:
                messages.error(request, 'Your payment could not be processed')
    else:
        payment_form = PaymentForm()
        order_form = OrderForm()

    return render(request, 'checkout.html', {'order_form': order_form,
                                             'payment_form': payment_form,
                                             'total': total,
                                             'publishable': settings.STRIPE_PUBLISHABLE})
