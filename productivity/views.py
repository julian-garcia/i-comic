from django.shortcuts import render
from tickets.models import Ticket
from .productivity import chart_data, group_by_date, min_date, top_n_tickets, tickets_date_range

def productivity(request):
    '''
    Generate ticket data to be used by JavaScript Chartist.js
    '''
    ticket_counts = group_by_date()

    # For the weekly/monthly chart, pick up the last 12/40 weeks worth of tickets based on the latest ticket raised
    weekly_min = min_date(12)
    monthly_min = min_date(40)

    # Tickets ordered by descending upvotes so the top N bugs/features can be listed
    top_tickets = Ticket.objects.values('id', 'title', 'type', 'upvotes', 'description').order_by('type', '-upvotes', 'title')

    # Generate chart data to feed in to Chartist.js (dictionary list of date/count key pair values)
    feature_data = chart_data(ticket_counts, 'Feature', 15)
    bug_data = chart_data(ticket_counts, 'Bug', 15)

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
