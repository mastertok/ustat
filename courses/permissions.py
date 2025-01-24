from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только для преподавателей.
    Для остальных - только чтение.
    """
    
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Проверяем аутентификацию и роль пользователя
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['teacher', 'producer']
        )
    
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Проверяем, является ли пользователь преподавателем курса
        if hasattr(obj, 'course'):
            course = obj.course
        else:
            course = obj
            
        return (
            request.user and
            request.user.is_authenticated and
            (
                request.user.role == 'producer' or
                (
                    request.user.role == 'teacher' and
                    course.get_primary_teacher() == request.user
                )
            )
        )
