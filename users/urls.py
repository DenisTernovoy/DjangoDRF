from rest_framework import routers

from users.views import CustomUserViewSet

app_name = "users"
user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet)

urlpatterns = []

urlpatterns += user_router.urls
