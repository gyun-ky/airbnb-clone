from django_countries import countries
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
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
    try : 
        room = models.Room.objects.get(pk=pk)
        ctx = {
            'room':room,
        }
        return render(request, "rooms/detail.html", ctx)
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))

def search(request):
    city = request.GET.get("city", "Anywhere")
    city= str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant =  bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    form = {
        "city":city,
        "s_country":country,
        "s_room_type":room_type,
        "price" : price,
        "guests" : guests,
        "bedrooms" : bedrooms,
        "beds" : beds,
        "baths" : baths,
        "s_amenities" : s_amenities,
        "s_facilities" : s_facilities,
        "instant" : instant,
        "superhost": super_host,
    }

    
    
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries":countries,
        "room_types":room_types,
        "amenities" : amenities,
        "facilities" : facilities,
        
    }
    filter_arg = {}

    if city != "Anywhere":
        filter_arg["city__startswith"] = city
    
    filter_arg["country"] = country

    if room_type != 0:
        filter_arg["room_type__pk__exact"] = room_type

    if price != 0:
        filter_arg["price_lte"] = price

    if guests != 0:
        filter_arg["guests_gte"] = guests

    if bedrooms != 0:
        filter_arg["bedrooms_gte"] = bedrooms
    
    if beds != 0:
        filter_arg["beds_gte"] = beds

    if baths != 0:
        filter_arg["baths_gte"] = baths

    if instant is True:
        filter_arg["instant_book"] = True
    
    if superhost is True:
        filter_arg["host__superhost"] = True
    rooms = models.Room.objects.filter(**filter_arg)
    results = {
        "rooms" : rooms,
    }

    if len(s_amenities)>0:
        for s_amenity in s_amenities :
            filter_args["amenities__pk"] = int(s_amenity)
    
    if len(s_facilities)>0:
        for s_facility in s_facilities :
            filter_args["facilities__pk"] = int(s_facility)
    return render(request,  "rooms/search.html", {**form, **choices, **results})