from rest_framework import serializers

from registration.models import (
    Registration,
    Event,
    Location,
    Review,
    EventMaterial,
    Organizer,
    Picture
)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'registration_date', 'status']

class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizer
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    #organizer = OrganizerSerializer(read_only = "True")
    #location = LocationSerializer(read_only = "True")
    class Meta:
        model = Event
        fields = [
            'id',
            'location',
            'organizer',
            'title',
            'description',
            'event_date',
            'max_participants',
            'image',
            'images',
            'status'
        ]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'event',
            'rating',
            'comment',
            'review_date'
        ]


class EventMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventMaterial
        fields = [
            'id',
            'event',
            'title',
            'description',
            'file',
            'material_date'
        ]

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image']

