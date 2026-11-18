from rest_framework import serializers
from django.contrib.auth.models import User

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

    def create(self, validated_data):
        if "request" in self.context:
            validated_data["user"] = self.context["request"].user

        return super().create(validated_data)
    
    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'registration_date', 'status']
        read_only_fields = ['user', 'registration_date']

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

    def create(self, validated_data):
        if "request" in self.context:
            validated_data["user"] = self.context["request"].user

        return super().create(validated_data)

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
        read_only_fields = ['user', 'review_date']


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

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']