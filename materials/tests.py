from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import CustomUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.ru", password="12345")
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test lesson",
            description="Test description",
            owner=self.user,
            course=self.course,
            url="https://youtube.com/some_params",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_lesson(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_update_lesson(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        params = {"name": "Test lesson NEW"}
        response = self.client.patch(url, data=params)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), params["name"])

    def test_create_lesson(self):
        url = reverse("materials:lesson-create")
        params = {
            "name": "Test lesson 2",
            "course": self.course.pk,
            "owner": self.user.pk,
            "url": "https://youtube.com/some_params",
        }
        response = self.client.post(url, data=params)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_delete_lesson(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.ru", password="12345")
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course": self.course.name})
        data = response.json()

        self.assertEqual(data.get("message"), "Подписка добавлена")

        response = self.client.post(url, {"course": self.course.name})
        data = response.json()
        self.assertEqual(data.get("message"), "Подписка удалена")
