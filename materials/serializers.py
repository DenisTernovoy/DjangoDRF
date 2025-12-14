from rest_framework import serializers
from materials.models import Course, Lesson
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
        if obj.course.exists():
            flag = "Подписка активна"
        else:
            flag = "Подписка неактивна"
        return flag

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
