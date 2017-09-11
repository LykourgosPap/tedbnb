from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAccountOwner(BasePermission):
    message = 'Login in as this user before changing it'

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user
        return False

class IsUserVerified(BasePermission):
    message = ''

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        else:
            if request.user:
                if request.user.type == 2:
                    self.message = 'User is not yet approved my admin'
                    return False

                if request.user.type == 0:
                    self.message = 'User is not renter type'
                    return False

                return True

class IsObjectOwner(BasePermission):
    message = 'User must be the owner of house'

    def has_object_permission(self, request, view, obj):
        return obj.userid.id == request.user.id
