from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    message = "You are not a moderator"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
