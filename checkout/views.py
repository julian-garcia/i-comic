from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm, PaymentForm
from .checkout import process_payment, commit_data

@login_required
def checkout(request):
    '''
    Combined payment form and order form to register new features and feature upvotes, both
    of which must be paid for by the end user.
    '''
    cart_upvotes = request.session.get('cart_upvotes', [])
    cart = request.session.get('cart', [])
    total = sum(float(i['cost']) for i in cart_upvotes) + sum(float(i['feature_cost']) for i in cart)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        order_form = OrderForm(request.POST)
        if payment_form.is_valid() and order_form.is_valid():
            # Process the payment using the Stripe API, feeding back any error messages
            # to this site if unsuccessful
            process_payment(request, total, payment_form)

            # Only if the Stripe payment is successful, save the order, features
            # and feature upvotes in the backend database
            if process_payment.charge_customer.paid:
                commit_data(request, order_form, cart, cart_upvotes)
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
