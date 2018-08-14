from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    '''
    Display the cart contents and calculate the overall total to
    facilitate checkout
    '''
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        cart = []

    if 'cart_upvotes' in request.session:
        cart_upvotes = request.session['cart_upvotes']
    else:
        cart_upvotes = []

    total = sum(float(item['feature_cost']) for item in cart) + sum(float(item['cost']) for item in cart_upvotes)
    return render(request, 'cart.html', {'cart': cart, 'cart_upvotes': cart_upvotes, 'total': total})

@login_required
def adjust_cart(request, title):
    '''
    Retrieve each proposed feature in the cart and amend its cost if the feature title matches
    the title against which the amount was changed
    '''
    new_cost = float(request.POST.get('cost'))
    cart = request.session.get('cart', [])

    for item in cart:
        if item['title'] == title:
            item['feature_cost'] = new_cost

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

@login_required
def adjust_upvote_cart(request, id):
    '''
    Retrieve each upvoted feature in the cart and amend its cost if the feature id matches
    the id against which the amount was changed
    '''
    new_cost = float(request.POST.get('cost'))
    cart_upvotes = request.session.get('cart_upvotes', [])

    for item in cart_upvotes:
        if item['id'] == int(id):
            item['cost'] = new_cost

    request.session['cart_upvotes'] = cart_upvotes
    return redirect(reverse('view_cart'))
