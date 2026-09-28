from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile

from registration.models import (
    Registration,
    Event,
    Location,
    Review,
    EventMaterial,
    Organizer
)

# Create your tests here.
class LocationViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        location = baker.make("Location")
            
        r = self.client.get('/api/locations/')
        data = r.json()
        print(data)

        assert location.name == data[0]['name']
        assert location.address == data[0]['address']
        assert location.capacity == data[0]['capacity']
        assert location.id == data[0]['id']
        assert len(data) == 1

    def test_create_location(self):
        r = self.client.post("/api/locations/", {
            "name": "Музей",
            "address": "ул. Маркова",
            "capacity": 47
        })

        new_location_id = r.json()['id']

        locations = Location.objects.all()
        assert len(locations) == 1 

        new_location = Location.objects.filter(id=new_location_id).first()
        assert new_location.name == "Музей"
        assert new_location.address == "ул. Маркова"
        assert new_location.capacity == 47

    def test_delete_location(self):
        locations = baker.make("Location", 10)
        r = self.client.get('/api/locations/')
        data = r.json()
        assert len(data) == 10

        location_id_to_delete = locations[3].id
        self.client.delete(f'/api/locations/{location_id_to_delete}/')

        r = self.client.get('/api/locations/')
        data = r.json()
        assert len(data) == 9
        
        assert location_id_to_delete not in [i['id'] for i in data]

    def test_update_location(self):
        locations = baker.make("Location", 10)
        location: Location = locations[2]

        r = self.client.get(f'/api/locations/{location.id}/')
        data = r.json()
        assert data['name'] == location.name

        r = self.client.put(f'/api/locations/{location.id}/', {
            "name": "Школа",
            "address": location.address,
            "capacity": location.capacity
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/locations/{location.id}/')
        data = r.json()
        assert data['name'] == "Школа"

        location.refresh_from_db()
        assert data['name'] == location.name

class EventViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "Event",
            location=location,
            organizer=organizer
        )

        r = self.client.get('/api/events/')
        data = r.json()
        print(data)

        assert event.location.id == data[0]['location']
        assert event.organizer.id == data[0]['organizer']
        assert event.title == data[0]['title']
        assert event.description == data[0]['description']
        assert event.max_participants == data[0]['max_participants']
        assert event.status == data[0]['status']
        assert len(data) == 1

    def test_create_event(self):
        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        r = self.client.post("/api/events/", {
            "location": location.id,
            "organizer": organizer.id,
            "title": "Литературный вечер",
            "description": "Вечер современной литературы",
            "event_date": "2026-10-15T18:00:00Z",
            "max_participants": 30,
            "status": "PLANNED"
        })

        new_event_id = r.json()['id']

        events = Event.objects.all()
        assert len(events) == 1

        new_event = Event.objects.filter(
            id=new_event_id
        ).first()

        assert new_event.location.id == location.id
        assert new_event.organizer.id == organizer.id
        assert new_event.title == "Литературный вечер"
        assert new_event.description == "Вечер современной литературы"
        assert new_event.max_participants == 30
        assert new_event.status == "PLANNED"

    def test_delete_event(self):
        events = baker.make("Event", 10)

        r = self.client.get('/api/events/')
        data = r.json()
        assert len(data) == 10

        event_id_to_delete = events[3].id

        self.client.delete(
            f'/api/events/{event_id_to_delete}/'
        )

        r = self.client.get('/api/events/')
        data = r.json()
        assert len(data) == 9

        assert event_id_to_delete not in [i['id'] for i in data]

    def test_update_event(self):
        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        events = baker.make(
            "Event",
            10,
            location=location,
            organizer=organizer
        )

        event: Event = events[2]

        r = self.client.get(
            f'/api/events/{event.id}/'
        )
        data = r.json()

        assert data['title'] == event.title

        r = self.client.put(
            f'/api/events/{event.id}/',
            {
                "location": event.location.id,
                "organizer": event.organizer.id,
                "title": "Обновленное мероприятие",
                "description": event.description,
                "event_date": event.event_date.isoformat(),
                "max_participants": event.max_participants,
                "status": event.status
            }
        )

        assert r.status_code == 200

        r = self.client.get(
            f'/api/events/{event.id}/'
        )
        data = r.json()

        assert data['title'] == "Обновленное мероприятие"

        event.refresh_from_db()

        assert data['title'] == event.title


class RegistrationViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        user = baker.make("auth.User")

        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")
        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        registration = baker.make(
            "Registration",
            user=user,
            event=event
        )

        r = self.client.get('/api/registrations/')
        data = r.json()
        print(data)

        assert registration.user.id == data[0]['user']
        assert registration.event.id == data[0]['event']
        assert registration.status == data[0]['status']
        assert len(data) == 1

    def test_create_registration(self):
        user = baker.make("auth.User")
        event = baker.make("registration.Event")

        r = self.client.post("/api/registrations/", {
            "user": user.id,
            "event": event.id,
            "status": "CREATED"
        })

        new_registration_id = r.json()['id']

        registrations = Registration.objects.all()
        assert len(registrations) == 1

        new_registration = Registration.objects.filter(
            id=new_registration_id
        ).first()

        assert new_registration.user.id == user.id
        assert new_registration.event.id == event.id
        assert new_registration.status == "CREATED"

    def test_delete_registration(self):
        registrations = baker.make("Registration", 10)

        r = self.client.get('/api/registrations/')
        data = r.json()
        assert len(data) == 10

        registration_id_to_delete = registrations[3].id

        self.client.delete(
            f'/api/registrations/{registration_id_to_delete}/'
        )

        r = self.client.get('/api/registrations/')
        data = r.json()
        assert len(data) == 9

        assert registration_id_to_delete not in [i['id'] for i in data]

    def test_update_registration(self):
        user = baker.make("auth.User")

        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        registrations = baker.make(
            "Registration",
            10,
            user=user,
            event=event
        )

        registration: Registration = registrations[2]

        r = self.client.get(
            f'/api/registrations/{registration.id}/'
        )
        data = r.json()

        assert data['status'] == registration.status

        r = self.client.put(
            f'/api/registrations/{registration.id}/',
            {
                "user": registration.user.id,
                "event": registration.event.id,
                "status": "CONFIRMED"
            }
        )

        assert r.status_code == 200

        r = self.client.get(
            f'/api/registrations/{registration.id}/'
        )
        data = r.json()

        assert data['status'] == "CONFIRMED"

        registration.refresh_from_db()

        assert data['status'] == registration.status

class ReviewViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        user = baker.make("auth.User")

        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        review = baker.make(
            "Review",
            user=user,
            event=event
        )

        r = self.client.get('/api/reviews/')
        data = r.json()
        print(data)

        assert review.user.id == data[0]['user']
        assert review.event.id == data[0]['event']
        assert str(review.rating) == data[0]['rating']
        assert review.comment == data[0]['comment']
        assert review.id == data[0]['id']
        assert len(data) == 1

    def test_create_review(self):
        user = baker.make("auth.User")
        event = baker.make("registration.Event")

        r = self.client.post("/api/reviews/", {
            "user": user.id,
            "event": event.id,
            "rating": "4.5",
            "comment": "Хорошее мероприятие"
        })

        new_review_id = r.json()['id']

        reviews = Review.objects.all()
        assert len(reviews) == 1

        new_review = Review.objects.filter(
            id=new_review_id
        ).first()

        assert new_review.user.id == user.id
        assert new_review.event.id == event.id
        assert new_review.rating == 4.5
        assert new_review.comment == "Хорошее мероприятие"

    def test_delete_review(self):
        reviews = baker.make("Review", 10)

        r = self.client.get('/api/reviews/')
        data = r.json()
        assert len(data) == 10

        review_id_to_delete = reviews[3].id

        self.client.delete(
            f'/api/reviews/{review_id_to_delete}/'
        )

        r = self.client.get('/api/reviews/')
        data = r.json()
        assert len(data) == 9

        assert review_id_to_delete not in [i['id'] for i in data]

    def test_update_review(self):
        user = baker.make("auth.User")

        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        reviews = baker.make(
            "Review",
            10,
            user=user,
            event=event
        )

        review: Review = reviews[2]

        r = self.client.get(
            f'/api/reviews/{review.id}/'
        )
        data = r.json()

        assert data['comment'] == review.comment

        r = self.client.put(
            f'/api/reviews/{review.id}/',
            {
                "user": review.user.id,
                "event": review.event.id,
                "rating": "5.0",
                "comment": "Отличное мероприятие"
            }
        )

        assert r.status_code == 200

        r = self.client.get(
            f'/api/reviews/{review.id}/'
        )
        data = r.json()

        assert data['rating'] == "5.0"
        assert data['comment'] == "Отличное мероприятие"

        review.refresh_from_db()

        assert str(review.rating) == data['rating']
        assert review.comment == data['comment']


class EventMaterialViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        file = SimpleUploadedFile(
            "program.pdf",
            b"test file content",
            content_type="application/pdf"
        )

        material = baker.make(
            "EventMaterial",
            event=event,
            file=file
        )

        r = self.client.get('/api/event-materials/')
        data = r.json()
        print(data)

        assert material.event.id == data[0]['event']
        assert material.title == data[0]['title']
        assert material.description == data[0]['description']
        assert material.id == data[0]['id']
        assert data[0]['file'].endswith(".pdf")
        assert len(data) == 1

    def test_create_event_material(self):
        event = baker.make("Event")

        file = SimpleUploadedFile(
            "program.pdf",
            b"test file content",
            content_type="application/pdf"
        )

        r = self.client.post(
            "/api/event-materials/",
            {
                "event": event.id,
                "title": "Программа мероприятия",
                "description": "Программа литературного вечера",
                "file": file
            },
            format="multipart"
        )

        assert r.status_code == 201

        new_material_id = r.json()['id']

        materials = EventMaterial.objects.all()
        assert len(materials) == 1

        new_material = EventMaterial.objects.filter(
            id=new_material_id
        ).first()

        assert new_material.event.id == event.id
        assert new_material.title == "Программа мероприятия"
        assert new_material.description == "Программа литературного вечера"
        assert new_material.file.name.endswith(".pdf")

    def test_delete_event_material(self):
        materials = baker.make("EventMaterial", 10)

        r = self.client.get('/api/event-materials/')
        data = r.json()
        assert len(data) == 10

        material_id_to_delete = materials[3].id

        self.client.delete(
            f'/api/event-materials/{material_id_to_delete}/'
        )

        r = self.client.get('/api/event-materials/')
        data = r.json()
        assert len(data) == 9

        assert material_id_to_delete not in [i['id'] for i in data]

    def test_update_event_material(self):
        location = baker.make("registration.Location")
        organizer = baker.make("registration.Organizer")

        event = baker.make(
            "registration.Event",
            location=location,
            organizer=organizer
        )

        materials = baker.make(
            "EventMaterial",
            10,
            event=event
        )

        material: EventMaterial = materials[2]

        r = self.client.get(
            f'/api/event-materials/{material.id}/'
        )
        data = r.json()

        assert data['title'] == material.title

        r = self.client.put(
            f'/api/event-materials/{material.id}/',
            {
                "event": material.event.id,
                "title": "Новая программа",
                "description": material.description
            }
        )

        assert r.status_code == 200

        r = self.client.get(
            f'/api/event-materials/{material.id}/'
        )
        data = r.json()

        assert data['title'] == "Новая программа"

        material.refresh_from_db()

        assert data['title'] == material.title


class OrganizerViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        organizer = baker.make("Organizer")

        r = self.client.get('/api/organizers/')
        data = r.json()
        print(data)

        assert organizer.name == data[0]['name']
        assert organizer.position == data[0]['position']
        assert organizer.phone == data[0]['phone']
        assert organizer.email == data[0]['email']
        assert organizer.id == data[0]['id']
        assert len(data) == 1

    def test_create_organizer(self):
        r = self.client.post("/api/organizers/", {
            "name": "Иванов Иван",
            "position": "Библиотекарь",
            "phone": "+79991234567",
            "email": "ivanov@gmail.com"
        })

        new_organizer_id = r.json()['id']

        organizers = Organizer.objects.all()
        assert len(organizers) == 1

        new_organizer = Organizer.objects.filter(
            id=new_organizer_id
        ).first()

        assert new_organizer.name == "Иванов Иван"
        assert new_organizer.position == "Библиотекарь"
        assert new_organizer.phone == "+79991234567"
        assert new_organizer.email == "ivanov@gmail.com"

    def test_delete_organizer(self):
        organizers = baker.make("Organizer", 10)

        r = self.client.get('/api/organizers/')
        data = r.json()
        assert len(data) == 10

        organizer_id_to_delete = organizers[3].id

        self.client.delete(
            f'/api/organizers/{organizer_id_to_delete}/'
        )

        r = self.client.get('/api/organizers/')
        data = r.json()
        assert len(data) == 9

        assert organizer_id_to_delete not in [i['id'] for i in data]

    def test_update_organizer(self):
        organizers = baker.make("Organizer", 10)
        organizer: Organizer = organizers[2]

        r = self.client.get(
            f'/api/organizers/{organizer.id}/'
        )
        data = r.json()
        assert data['name'] == organizer.name

        r = self.client.put(
            f'/api/organizers/{organizer.id}/',
            {
                "name": "Петров Петр",
                "position": organizer.position,
                "phone": organizer.phone,
                "email": organizer.email
            }
        )
        assert r.status_code == 200

        r = self.client.get(
            f'/api/organizers/{organizer.id}/'
        )
        data = r.json()
        assert data['name'] == "Петров Петр"

        organizer.refresh_from_db()
        assert data['name'] == organizer.name

