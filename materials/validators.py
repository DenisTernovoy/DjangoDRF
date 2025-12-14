from rest_framework.serializers import ValidationError


class LessonValidator:
    def __init__(self, url):
        self.url = url

    def __call__(self, value):
        reformatted_value = dict(value).get("url")
        if reformatted_value:
            if "youtube.com" not in reformatted_value:
                raise ValidationError(
                    "Нельзя использовать сторонние ссылки на материалы"
                )
