from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketAddForm, TicketEditForm, TicketCommentAddForm
from .models import Ticket, TicketComment, TicketUpvoter

def ticket_listing(request):
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
    ticket = Ticket.objects.get(pk=id)
    comments = TicketComment.objects.all().filter(ticket=ticket).order_by('-date_comment')

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
    ticket = Ticket.objects.get(pk=id)
    upvotes = TicketUpvoter.objects.all().filter(upvoter_ticket=ticket,
                                                 upvoter_user=request.user)
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
