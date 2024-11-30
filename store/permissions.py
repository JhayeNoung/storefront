from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access for all users
    and write access only for admin users.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS (e.g., GET, HEAD, OPTIONS) are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed for admin users
        return bool(request.user and request.user.is_staff)
    
class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("store.view_history") # return True if user has the custom permission in the Meta Option of Customer Model

'''
has_perm(perm, obj=None)
Returns True if the user has the specified permission, where perm is in the format 
"<app label>.<permission codename>". (see documentation on permissions). If the user is inactive, this method will 
always return False. For an active superuser, this method will always return True.

If obj is passed in, this method won't check for a permission for the model, but for this specific object.

(https://docs.djangoproject.com/en/5.1/ref/contrib/auth/#methods)
'''