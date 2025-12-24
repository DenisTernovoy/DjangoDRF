from rest_framework.serializers import ValidationError


class PaymentValidator:
    def __init__(self, course, lesson):
        self.course = course
        self.lesson = lesson

    def __call__(self, value):
        lesson = dict(value).get("lesson")
        course = dict(value).get("course")

        if not course and not lesson:
            raise ValidationError("Необходимо выбрать или курс или урок")
        if course and lesson:
            raise ValidationError("Необходимо указать что-то одно: курс или урок")
