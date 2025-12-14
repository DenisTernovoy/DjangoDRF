from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="preview/", verbose_name="Превью", null=True, blank=True
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", null=True, blank=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(
        max_length=100, verbose_name="Описание", null=True, blank=True
    )
    preview = models.ImageField(
        upload_to="preview/", verbose_name="Превью", null=True, blank=True
    )
    url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="course"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.subscriber} - {self.course.name}"
