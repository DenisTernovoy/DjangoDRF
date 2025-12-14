from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "count_lesson", "lessons")
