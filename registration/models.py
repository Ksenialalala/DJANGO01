from django.db import models

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
        

class Event(models.Model):
    location = models.ForeignKey("registration.Location", on_delete=models.CASCADE, null=True, verbose_name = "Локация")
    organizer = models.ForeignKey("registration.Organizer", on_delete=models.CASCADE, null=True, verbose_name = "Организатор")
    title = models.TextField("Название")
    description = models.TextField("Описание")
    event_date = models.DateTimeField("Дата")
    max_participants = models.IntegerField("Количество участников")
    class StatusType(models.TextChoices):
        PLANNED = "PLANNED", "Запланировано"
        COMPLETED = "COMPLETED", "Завершено"
        CANCELLED = "CANCELLED", "Отменено"
    status = models.TextField("Статус", choices=StatusType.choices, default=StatusType.PLANNED)
    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

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
    file_path = models.TextField("Путь к файлу")
    material_type = models.TextField("Тип")
    material_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

class Organizer(models.Model):
    name = models.TextField("ФИО")
    position = models.TextField("Должность")
    phone = models.TextField("Номер")
    email = models.TextField("Почта")
    class Meta:
        verbose_name = "Организатор"
        verbose_name_plural = "Организаторы"
        
    def __str__(self) -> str:
            return self.name