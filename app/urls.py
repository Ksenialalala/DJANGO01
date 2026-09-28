"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from registration import views
from rest_framework.routers import DefaultRouter

from registration.api import (
    LocationsViewset,
    EventsViewset,
    RegistrationsViewset,
    ReviewsViewset,
    EventMaterialsViewset,
    OrganizersViewset
)

router = DefaultRouter()
router.register("locations", LocationsViewset, basename="locations")
router.register("events", EventsViewset, basename="events")
router.register("registrations", RegistrationsViewset, basename="registrations")
router.register("reviews", ReviewsViewset, basename="reviews")
router.register("event-materials", EventMaterialsViewset, basename="event-materials")
router.register("organizers", OrganizersViewset, basename="organizers")


urlpatterns = [
    path('', views.show_registration),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)