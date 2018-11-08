import os, datetime
from datetime import timedelta
from django.db.models import Count, Max
from tickets.models import Ticket

def top_n_tickets(type, tickets, num_tickets):
    '''
    Retrieve the first N tickets within a list of tickets
    '''
    return [{'title': item['title'],
                           'upvotes': item['upvotes'],
                           'id': item['id'],
                           'description': item['description']}
                            for item in tickets
                                if item['type']==type and
                                   item['upvotes'] is not None][:num_tickets]

def tickets_date_range(type, min_date, tickets):
    '''
    Retrieve a subset of tickets within a list of tickets with a date
    raised greater than a specified date
    '''
    return [{'dt_raised': item['dt_raised'],
               'ticket_count': item['ticket_count']}
               for item in tickets
                    if item['type']==type and
                        datetime.datetime.strptime(str(item['dt_raised']),'%Y-%m-%d').date() >= min_date]

def group_by_date():
    '''
    Group ticket counts by date raised and type (feature/bug) - this will be used
    to build line charts indicating productivity levels over time
    '''
    if os.environ.get('LOCAL'):
        return Ticket.objects.extra({'dt_raised' : "date(date_raised)"}).values('dt_raised','type').annotate(ticket_count=Count('id')).order_by('dt_raised')
    else:
        # Production app uses Postgresql db so need to use to_char function to
        # extract the date part of the date time stamp
        return Ticket.objects.extra({'dt_raised' : "to_char(date_raised,'yyyy-mm-dd')"}).values('dt_raised','type').annotate(ticket_count=Count('id')).order_by('dt_raised')

def min_date(n):
    '''
    Calculate the earliest date in a date range based on the latest date available
    '''
    return Ticket.objects.aggregate(Max('date_raised'))['date_raised__max'] - timedelta(weeks=n)

def chart_data(ticket_counts, ticket_type, n):
    '''
    Chart data to be passed to the JavaScript chart rendering code
    The line chart of daily tickets is based simply on the latest 15 tickets raised,
    needs to be done separately for bugs and features. Otherwise the latest 30 tickets
    may consist more of one ticket type
    '''
    return [{'dt_raised': item['dt_raised'],
             'ticket_count': item['ticket_count']}
            for item in ticket_counts if item['type']==ticket_type][(n * -1):]