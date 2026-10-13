from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

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