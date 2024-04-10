from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    login = models.EmailField(
        unique=True, max_length=100, blank=False, null=False, verbose_name="Логин"
    )
    password = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name="Пароль"
    )
    USERNAME_FIELD = "login"

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"


class Diary(models.Model):
    class KindField(models.TextChoices):
        PUBLIC = "PUBLIC"
        PRIVATE = "PRIVATE"

    title = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Название дневника"
    )
    expiration = models.DateField(blank=True, null=True, verbose_name="Дата истечения")
    kind = models.CharField(
        max_length=7,
        null=False,
        blank=False,
        choices=KindField.choices,
        verbose_name="Тип дневника",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="diaries",
        verbose_name="Пользователь",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Дневник"
        verbose_name_plural = "Дневники"


class Note(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name="Текст записи")
    diary = models.ForeignKey(
        Diary, on_delete=models.CASCADE, related_name="notes", verbose_name="Дневник"
    )

    def __str__(self):
        return f"Note {self.pk} - {self.diary.title}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
