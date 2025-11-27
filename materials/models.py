from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="preview/", verbose_name="Превью", null=True, blank=True
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", null=True, blank=True
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
