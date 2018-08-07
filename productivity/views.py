from django.shortcuts import render
from django.db.models import Count
from tickets.models import Ticket

def top_tickets():
    global top_feature_data, top_bug_data
    top_tickets = Ticket.objects.values('id', 'title', 'type', 'upvotes', 'description').order_by('type', '-upvotes', 'title')

    top_feature_data = [{'title': item['title'],
                         'upvotes': item['upvotes'],
                         'id': item['id'],
                         'description': item['description']}
                        for item in top_tickets
                            if item['type']=='Feature' and
                               item['upvotes'] is not None][:5]

    top_bug_data = [{'title': item['title'],
                     'upvotes': item['upvotes'],
                     'id': item['id'],
                     'description': item['description']}
                    for item in top_tickets
                        if item['type']=='Bug' and
                           item['upvotes'] is not None][:5]

def productivity(request):
    ticket_counts = Ticket.objects.extra({'dt_raised' : "date(date_raised)"}).values('dt_raised','type').annotate(ticket_count=Count('id')).order_by('dt_raised')

    feature_data = [{'dt_raised': item['dt_raised'],
                     'ticket_count': item['ticket_count']}
                    for item in ticket_counts if item['type']=='Feature'][-15:]

    bug_data = [{'dt_raised': item['dt_raised'],
                 'ticket_count': item['ticket_count']}
                for item in ticket_counts if item['type']=='Bug'][-15:]
    top_tickets()
    return render(request, 'productivity.html',
                  {'feature_data': feature_data,
                   'bug_data': bug_data,
                   'top_feature_data': top_feature_data,
                   'top_bug_data': top_bug_data})
