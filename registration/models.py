from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.IntegerChoices):
        undefined = 0
        participant = 1
        administrator = 2

    user = models.OneToOneField("auth.User",  on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField("Роль", choices=Role, default=Role.undefined)

    def __str__(self):
         return self.user.username if self.user else f"Profile {self.id}"
    

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
     if created:
          Profile.objects.create(user=instance, role=Profile.Role.undefined)

# Create your models here.
class Registration(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, verbose_name = "Пользователь")
    event = models.ForeignKey("registration.Event", on_delete=models.CASCADE, null=True, verbose_name = "Мероприятие")
    registration_date = models.DateTimeField(auto_now_add=True)
    class StatusType(models.TextChoices):
        CREATED = "CREATED", "Создана"
        CONFIRMED = "CONFIRMED", "Подтверждена"
        CANCELLED = "CANCELLED", "Отменена"
        COMPLETED = "COMPLETED", "Завершена"
    status = models.TextField("Статус", choices=StatusType.choices, default=StatusType.CREATED)
    class Meta:
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"

    def __str__(self) -> str:
            return self.event.title
        

class Event(models.Model):
    location = models.ForeignKey("registration.Location", on_delete=models.CASCADE, null=True, verbose_name = "Локация")
    organizer = models.ForeignKey("registration.Organizer", on_delete=models.CASCADE, null=True, verbose_name = "Организатор")
    title = models.TextField("Название")
    description = models.TextField("Описание")
    event_date = models.DateTimeField("Дата")
    max_participants = models.IntegerField("Количество участников")
    image = models.ImageField("Картинка", null=True, blank=True, upload_to='events/')
    images = models.ManyToManyField("Picture", blank=True, related_name="events")
    class StatusType(models.TextChoices):
        PLANNED = "PLANNED", "Запланировано"
        COMPLETED = "COMPLETED", "Завершено"
        CANCELLED = "CANCELLED", "Отменено"
    status = models.TextField("Статус", choices=StatusType.choices, default=StatusType.PLANNED)
    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self) -> str:
        return self.title
    
        

class Location(models.Model):
    name = models.TextField("Название")
    address = models.TextField("Адрес")
    capacity = models.IntegerField("Вместимость")
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self) -> str:
            return self.name

class Review(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, verbose_name = "Пользователь")
    event = models.ForeignKey("registration.Event", on_delete=models.CASCADE, null=True, verbose_name = "Мероприятие")
    rating = models.DecimalField("Оценка", max_digits=2, decimal_places=1)
    comment = models.TextField("Комментарий")
    review_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    
class EventMaterial(models.Model):
    event = models.ForeignKey("registration.Event", on_delete=models.CASCADE, null=True, verbose_name = "Мероприятие")
    title = models.TextField("Название")
    description = models.TextField("Описание")
    file = models.FileField("Файл", null=True, blank=True, upload_to="event_materials/")
    material_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    

class Organizer(models.Model):
    name = models.TextField("ФИО")
    position = models.TextField("Должность")
    phone = models.TextField("Номер")
    email = models.TextField("Почта")
    image = models.ImageField("Фото", null=True, blank=True, upload_to="organizers/")
    class Meta:
        verbose_name = "Организатор"
        verbose_name_plural = "Организаторы"
        
    def __str__(self) -> str:
            return self.name

class Picture(models.Model):
    image = models.ImageField(upload_to="event_photos/")

    def __str__(self):
        return f"Фото {self.id}"