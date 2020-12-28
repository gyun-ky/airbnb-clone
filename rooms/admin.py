from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . import models
from django.utils.html import mark_safe

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""
    list_display=(
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

class PhotoInline(admin.TabularInline):
    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ RoomAdmin Definition """
    inlines = [PhotoInline, ]

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price", "room_type")}
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book", )}
        ),
        (
            "More About the Space",
            {"fields" : ("guests", "beds", "bedrooms", "baths",)}
        ),
        (
            "Spaces",
            {"fields": ("amenities", "facilities", "house_rules",)}
        ),
        (
            "Last Details",
            {"fields":("host",)}
        )
        
    )

    ordering = ('name', 'price', 'bedrooms', )

    filter_horizontal = (
        "amenities", 
        "facilities", 
        "house_rules",
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book", 
        "room_type", 
        "amenities", 
        "facilities", 
        "house_rules", 
        "city", 
        "country" )

    raw_id_fields = ("host",)

    search_fields = ("^city", "^host__username")

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Hello Sexy"

    def count_photos(self, obj):
        return obj.photos.count()
    
 
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """photo Admin Definition"""

    list_display = ('__str__', 'get_thumbnail',)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')
    get_thumbnail.short_description = "Thumbnail"