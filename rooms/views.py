from datetime import datetime
from django.shortcuts import render, redirect
from . import models
from math import ceil
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

def all_rooms(request):
    page = int(request.GET.get("page", 1))
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 2)
    try:
        page = paginator.page(page)
        ctx = {
        "page":page,
        }
        return render(request, "rooms/home.html", ctx)
    except EmptyPage:
        page = paginator.page(1)
        redirect('/')
    
    # page = int(request.GET.get("page", '1'))
    # page_size = 2
    # limit = page * page_size
    # offset = limit - page_size
    # all_rooms = models.Room.objects.all()[offset:limit]

    # page_count = models.Room.objects.count()/2
    # ctx = {
    #     "all_rooms" : all_rooms,
    #     "page":page,
    #     "page_count":ceil(page_count),
    #     "page_range":range(1, ceil(page_count)+1),
    #}
    # return render(request, "rooms/home.html", ctx)

    def room_detail(request, pk):
        
        ctx = {

        }
        return render(request, "rooms/detail.html", ctx)
