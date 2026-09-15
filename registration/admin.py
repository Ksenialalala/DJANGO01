from django.contrib import admin

from registration.models import (
    Registration, 
    Event,
    Location,
    Review,
    EventMaterial,
    Organizer
)

# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'status']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'location', 
        'organizer', 
        'title', 
        'description', 
        'event_date', 
        'max_participants', 
        'status'
    ]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'capacity']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'rating', 'comment', 'review_date']


@admin.register(EventMaterial)
class EventMaterialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'event',
        'title',
        'description',
        'file_path',
        'material_type',
        'material_date'
    ]


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'phone', 'email']