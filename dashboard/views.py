# coding=utf-8

import json
import time
import calendar
import datetime

from os.path import dirname, join, realpath, getmtime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F, Count, Sum

from dashboard.models import Rep, Stat, Event, FunctionalArea, Goal, Metric, EventMetric

PROJECT_PATH = realpath(join(dirname(__file__), '..'))
FILE = PROJECT_PATH + '/reps.json'

def home(request):
    
    
    context = {
    }

    return render(request, 'dashboard/home.html', context)

def event_metrics(request):
    
    # We expect events that took place at least 3 days ago to have metrics
    end_date = datetime.datetime.now() - datetime.timedelta(days=3)
    
    # Get events between Jan. 2014 and today.
    events = Event.objects.filter(start__gte=datetime.datetime(2014, 6, 16, 0, 0, 0, 0), start__lt=end_date).order_by('start')
    
    # Events that haven't filled post-event metrics, we exclude deleted Reps.
    need_metrics = Event.objects.filter(actual_attendance=None, start__gte=datetime.datetime(2014, 6, 16, 0, 0, 0, 0), start__lt=end_date).order_by('owner__first_name').exclude(owner=None)
    
    # Percentage of pending events
    pending = 100 - round( need_metrics.count() * 100.0 / events.count(), 2 )
    
    # Reps who completed their metrics
    awesome_reps = Rep.objects.filter(event__start__gte=datetime.datetime(2014, 6, 16, 0, 0, 0, 0), event__start__lt=end_date).exclude(event__actual_attendance=None).annotate(num_events=Count('event')).order_by('-num_events')[:5]
    
    context = {
        'events': events,
        'need_metrics': need_metrics,
        'pending': pending,
        'end_date': end_date,
        'reps': awesome_reps,
    }
    
    return render(request, 'dashboard/event-metrics.html', context)
