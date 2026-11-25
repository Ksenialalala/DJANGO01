from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets, pagination, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from registration.models import Profile

from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate

from .serializers import ParticipantSerializer

from registration.models import (
    Registration,
    Event,
    Location,
    Review,
    EventMaterial,
    Organizer,
    Picture
)

from registration.serializers import (
    RegistrationSerializer,
    EventSerializer,
    LocationSerializer,
    ReviewSerializer,
    EventMaterialSerializer,
    OrganizerSerializer,
    PictureSerializer
)

class ParticipantsViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.filter(
        profile__role=Profile.Role.participant
    ).select_related('profile')

    serializer_class = ParticipantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        event_id = self.request.query_params.get('event')

        if event_id:
            participants_ids = Registration.objects.filter(
                event_id=event_id
            ).values_list('user_id', flat=True)

            queryset = queryset.filter(id__in=participants_ids)

        return queryset


class RegistrationsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.profile.role == Profile.Role.administrator:
            return queryset

        queryset = queryset.filter(user=self.request.user)

        return queryset


class EventsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, url_path='register', methods=['POST'])
    def register(self, *args, **kwargs):
        event = self.get_object()
        Registration.objects.create(
            user=self.request.user,
            event=event,
        )

        return Response()


class LocationsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ReviewsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.profile.role == Profile.Role.administrator:
            return queryset

        queryset = queryset.filter(user=self.request.user)

        return queryset


class EventMaterialsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = EventMaterial.objects.all()
    serializer_class = EventMaterialSerializer


class OrganizersViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

class PicturesViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path="me", methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data={
            'is_authenticated': self.request.user.is_authenticated
        }

        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "role": self.request.user.profile.role
            })


        return Response(data=data)

    @action(detail=False, url_path="logout", methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)

        return Response()

    @action(detail=False, url_path="login", methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        success = False
        starus_code = 403

        user = authenticate(username=username, password=password)
        if user:
            success = True
            starus_code = 200
            django_login(self.request, user)

        return Response({
            'success': success
        }, status=starus_code)
    #me
    #login
    #logout
