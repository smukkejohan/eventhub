# -*- coding: utf-8 -*-

from django.db.models.aggregates import Count
from taggit.views import tagged_object_list
from events.models import Event, Category
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import list_detail, date_based
import settings

PAGINATE_BY = getattr(settings, 'PAGINATE_BY', 12)

def past(request):
    
    past = Event.public_objects.past()
    
    return render(request, "events/past.html", {
        'past': past})
    
    
    
def by_category(request, slug, **kwargs):
    cat = get_object_or_404(Category, slug=slug)
    
    future = Event.public_objects.future().filter(categories__name__in=[cat.name]).distinct()    
    featured = []
    try:
        featured = future.filter(featured=True)[:1][0]
        future = future.exclude(id=featured.id)
    except IndexError:
        pass        
    
    return render(request, "events/by_category.html", {
        'category': cat, 'future': future, 'featured': featured})
    

def index(request, **kwargs):
    future = Event.public_objects.future()    
    featured = []
    try:
        featured = future.filter(featured=True)[:1][0]
        future = future.exclude(id=featured.id)
    except IndexError:
        pass        
    
    return render(request, "index.html", {'future': future, 'featured': featured})

def detail(request, year, month, day, slug):
    if request.user.is_staff:
        qs = Event.objects
    else:
        qs = Event.public_objects

    event = get_object_or_404(qs, start__year=year, start__month=month, start__day=day, slug=slug)

    return render(request, "events/detail.html", {'object': event})


    

