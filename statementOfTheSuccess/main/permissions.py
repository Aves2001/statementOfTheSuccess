from rest_framework import permissions


class isCuratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name='Деканат').exists():
            # if request.user != Record.objects.filter(pk=self.kwargs['pk']).get().teacher:
            return False
        return True
