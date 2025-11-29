from rest_framework import routers
from materials.apps import MaterialsConfig
from materials import views
from django.urls import path

app_name = MaterialsConfig.name

material_router = routers.DefaultRouter()
material_router.register(r"courses", views.CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", views.LessonListAPIView.as_view(), name="lessons"),
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
    path(
        "lessons/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-detail"
    ),
    path(
        "lessons/<int:pk>/update/",
        views.LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        views.LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
]

urlpatterns += material_router.urls
