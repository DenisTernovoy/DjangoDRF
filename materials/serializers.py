from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            LessonValidator("url"),
        ]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_count_lesson(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(subscriber=user, course=obj).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "count_lesson",
            "lessons",
            "subscription",
        )
