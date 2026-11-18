
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transliterate import translit

from faker import Faker
import random
import re
from tqdm import tqdm

from registration.models import (
    Profile,
    Location,
    Organizer,
    Event,
    Registration,
    Review,
    EventMaterial
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker('ru_RU')

        for i in tqdm(range(1000)):
            fio = fake.name()

            fio_translited = translit(fio, 'ru', reversed=True).lower()
            fio_translited = re.sub("['-]", "", fio_translited)
            fio_translited = fio_translited.replace(" ", "_")

            username = f"participant_{fio_translited}_{i}"

            splitted_name = fio.split(" ")

            if len(splitted_name) != 3:
                fio = fake.last_name() + " " + fake.first_name() + " " + fake.middle_name()
                splitted_name = fio.split(" ")

            first_name, last_name, _ = splitted_name

            user = User.objects.create_user(
                username=username,
                email=f"{username}@yandex.ru",
                first_name=first_name,
                last_name=last_name,
                password="123"
            )

            user.profile.role = Profile.Role.participant
            user.profile.save()

        users = list(User.objects.filter(profile__role=Profile.Role.participant))

        locations = []
        for _ in tqdm(range(1000)):
            locations.append(Location.objects.create(
                name=fake.company(),
                address=fake.address(),
                capacity=random.randint(20, 500)
            ))

        organizers = []
        for _ in tqdm(range(1000)):
            organizers.append(Organizer.objects.create(
                name=fake.name(),
                position=fake.job(),
                phone=fake.phone_number(),
                email=fake.unique.email()
            ))

        events = []
        for _ in tqdm(range(1000)):
            events.append(Event.objects.create(
                location=random.choice(locations),
                organizer=random.choice(organizers),
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=300),
                event_date=fake.date_time_between(
                    start_date="-2y",
                    end_date="+1y"
                ),
                max_participants=random.randint(20, 200),
                status=random.choice([
                    Event.StatusType.PLANNED,
                    Event.StatusType.COMPLETED,
                    Event.StatusType.CANCELLED
                ])
            ))

        for _ in tqdm(range(1000)):
            Registration.objects.create(
                user=random.choice(users),
                event=random.choice(events),
                status=random.choice([
                    Registration.StatusType.CREATED,
                    Registration.StatusType.CONFIRMED,
                    Registration.StatusType.CANCELLED,
                    Registration.StatusType.COMPLETED
                ])
            )

        for _ in tqdm(range(1000)):
            Review.objects.create(
                user=random.choice(users),
                event=random.choice(events),
                rating=round(random.uniform(1, 5), 1),
                comment=fake.text(max_nb_chars=300)
            )

        for _ in tqdm(range(1000)):
            EventMaterial.objects.create(
                event=random.choice(events),
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=300)
            )

