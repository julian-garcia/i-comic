from django.shortcuts import render
from django.db.models import Count, Max
from datetime import timedelta
import datetime
from tickets.models import Ticket

def top_n_tickets(type, tickets, num_tickets):
    # Retrieve the first N tickets within a list of tickets
    return [{'title': item['title'],
                           'upvotes': item['upvotes'],
                           'id': item['id'],
                           'description': item['description']}
                            for item in tickets
                                if item['type']==type and
                                   item['upvotes'] is not None][:num_tickets]

def tickets_date_range(type, min_date, tickets):
    # Retrieve a subset of tickets within a list of tickets with a date
    # raised greater than a specified date
    return [{'dt_raised': item['dt_raised'],
               'ticket_count': item['ticket_count']}
               for item in tickets
                    if item['type']==type and
                        datetime.datetime.strptime(item['dt_raised'],'%Y-%m-%d').date() >= min_date]

def productivity(request):
    '''
    Generate ticket data to be used by JavaScript Chartist.js
    '''
    # Group ticket counts by date raised and type (feature/bug) - this will be used
    # to build line charts indicating productivity levels over time
    ticket_counts = Ticket.objects.extra({'dt_raised' : "date(date_raised)"}).values('dt_raised','type').annotate(ticket_count=Count('id')).order_by('dt_raised')
    # For the weekly/monthly chart, pick up the last 12/40 weeks worth of tickets based on the latest ticket raised
    weekly_min = Ticket.objects.aggregate(Max('date_raised'))['date_raised__max'] - timedelta(weeks=12)
    monthly_min = Ticket.objects.aggregate(Max('date_raised'))['date_raised__max'] - timedelta(weeks=40)
    # Tickets ordered by descending upvotes so the top N bugs/features can be listed
    top_tickets = Ticket.objects.values('id', 'title', 'type', 'upvotes', 'description').order_by('type', '-upvotes', 'title')

    # The line chart of daily tickets is based simply on the latest 15 tickets raised,
    # needs to be done separately for bugs and features. Otherwise the latest 30 tickets
    # may consist more of one ticket type
    feature_data = [{'dt_raised': item['dt_raised'],
                     'ticket_count': item['ticket_count']}
                    for item in ticket_counts if item['type']=='Feature'][-15:]

    bug_data = [{'dt_raised': item['dt_raised'],
                 'ticket_count': item['ticket_count']}
                for item in ticket_counts if item['type']=='Bug'][-15:]

    # Apply weekly/monthly date ranges and split the data in to features/bugs
    feature_data_weekly = tickets_date_range('Feature', weekly_min.date(), ticket_counts)
    feature_data_monthly = tickets_date_range('Feature', monthly_min.date(), ticket_counts)
    bug_data_weekly = tickets_date_range('Bug', weekly_min.date(), ticket_counts)
    bug_data_monthly = tickets_date_range('Bug', monthly_min.date(), ticket_counts)

    top_feature_data = top_n_tickets('Feature', top_tickets, 5)
    top_bug_data = top_n_tickets('Bug', top_tickets, 5)

    return render(request, 'productivity.html',
                  {'feature_data': feature_data,
                   'bug_data': bug_data,
                   'top_feature_data': top_feature_data,
                   'top_bug_data': top_bug_data,
                   'feature_data_weekly': feature_data_weekly,
                   'feature_data_monthly': feature_data_monthly,
                   'bug_data_weekly': bug_data_weekly,
                   'bug_data_monthly': bug_data_monthly})
