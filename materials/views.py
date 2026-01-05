from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonAndCoursePaginator
from materials.serializers import (CourseCountSerializer, CourseSerializer,
                                   LessonSerializer)
from materials.services import get_recipient_list
from materials.tasks import send_email_notice, send_information_about_course
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):

    pagination_class = LessonAndCoursePaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseCountSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action == "destroy":
            self.permission_classes = [~IsModer & IsOwner]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]
        return super().get_permissions()

    def get_queryset(self):
        if IsModer in self.permission_classes:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.last_update = timezone.now()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        user_list_email = get_recipient_list(instance.pk)
        send_information_about_course.delay(user_list_email)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonAndCoursePaginator

    def get_queryset(self):
        if IsModer in self.permission_classes:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user.id)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        course = instance.course.pk
        send_email_notice.delay(course)

        return Response(serializer.data)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class SubscribeView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        course = get_object_or_404(Course.objects.all(), name=data["course"])
        sub = Subscription.objects.filter(subscriber=user, course=course)

        if sub.exists():
            sub.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(subscriber=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
