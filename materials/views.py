from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseCountSerializer,
)
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):

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


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner, ~IsModer)


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
