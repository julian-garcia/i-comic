from django.shortcuts import render
from django.db.models import Count, Max
from datetime import timedelta
import datetime
from tickets.models import Ticket

def top_tickets(type):
    top_tickets = Ticket.objects.values('id', 'title', 'type', 'upvotes', 'description').order_by('type', '-upvotes', 'title')

    return [{'title': item['title'],
                           'upvotes': item['upvotes'],
                           'id': item['id'],
                           'description': item['description']}
                            for item in top_tickets
                                if item['type']==type and
                                   item['upvotes'] is not None][:5]

def tickets_date_range(type, min_date, tickets):
    return [{'dt_raised': item['dt_raised'],
               'ticket_count': item['ticket_count']}
               for item in tickets
                    if item['type']==type and
                        datetime.datetime.strptime(item['dt_raised'],'%Y-%m-%d').date() >= min_date]

def productivity(request):
    ticket_counts = Ticket.objects.extra({'dt_raised' : "date(date_raised)"}).values('dt_raised','type').annotate(ticket_count=Count('id')).order_by('dt_raised')
    weekly_min = Ticket.objects.aggregate(Max('date_raised'))['date_raised__max'] - timedelta(weeks=12)
    monthly_min = Ticket.objects.aggregate(Max('date_raised'))['date_raised__max'] - timedelta(weeks=24)

    feature_data = [{'dt_raised': item['dt_raised'],
                     'ticket_count': item['ticket_count']}
                    for item in ticket_counts if item['type']=='Feature'][-15:]

    bug_data = [{'dt_raised': item['dt_raised'],
                 'ticket_count': item['ticket_count']}
                for item in ticket_counts if item['type']=='Bug'][-15:]

    feature_data_weekly = tickets_date_range('Feature', weekly_min.date(), ticket_counts)
    feature_data_monthly = tickets_date_range('Feature', monthly_min.date(), ticket_counts)
    bug_data_weekly = tickets_date_range('Bug', weekly_min.date(), ticket_counts)
    bug_data_monthly = tickets_date_range('Bug', monthly_min.date(), ticket_counts)

    top_feature_data = top_tickets('Feature')
    top_bug_data = top_tickets('Bug')

    return render(request, 'productivity.html',
                  {'feature_data': feature_data,
                   'bug_data': bug_data,
                   'top_feature_data': top_feature_data,
                   'top_bug_data': top_bug_data,
                   'feature_data_weekly': feature_data_weekly,
                   'feature_data_monthly': feature_data_monthly,
                   'bug_data_weekly': bug_data_weekly,
                   'bug_data_monthly': bug_data_monthly})
