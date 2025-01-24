from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.conf import settings
from typing import Tuple, Optional
import jwt
from datetime import datetime, timedelta

class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация на основе JWT токенов с поддержкой автоматического обновления
    """
    
    def authenticate(self, request) -> Optional[Tuple]:
        """
        Аутентификация пользователя по JWT токену
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
            
        try:
            # Извлекаем токен
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                return None
            token = auth_parts[1]
            
            # Проверяем токен
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            # Проверяем срок действия
            exp = datetime.fromtimestamp(payload['exp'])
            if exp < timezone.now():
                raise AuthenticationFailed('Token has expired')
                
            # Получаем пользователя
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=payload['user_id'])
            
            # Проверяем необходимость обновления токена
            if self._should_refresh_token(exp):
                new_token = self.generate_token(user)
                # Добавляем новый токен в заголовок ответа
                request.new_token = new_token
                
            return (user, token)
            
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return None
            
    def _should_refresh_token(self, exp_time: datetime) -> bool:
        """
        Проверяет, нужно ли обновить токен
        """
        refresh_threshold = timezone.now() + timedelta(minutes=30)
        return exp_time < refresh_threshold
        
    @staticmethod
    def generate_token(user) -> str:
        """
        Генерация нового JWT токена
        """
        payload = {
            'user_id': user.id,
            'exp': int((timezone.now() + timedelta(hours=24)).timestamp()),
            'iat': int(timezone.now().timestamp()),
            'role': user.role
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


class RoleBasedPermission(BasePermission):
    """
    Проверка прав доступа на основе роли пользователя
    """
    
    def has_permission(self, request, view) -> bool:
        # Проверяем аутентификацию
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Получаем требуемые роли из атрибутов view
        required_roles = getattr(view, 'required_roles', None)
        if not required_roles:
            return True
            
        return request.user.role in required_roles


class MFARequired(BasePermission):
    """
    Проверка двухфакторной аутентификации для определенных ролей
    """
    
    def has_permission(self, request, view) -> bool:
        user = request.user
        
        # Проверяем, требуется ли MFA для роли пользователя
        if user.role in ['admin', 'teacher']:
            # Проверяем наличие MFA токена в заголовке
            mfa_token = request.headers.get('X-MFA-Token')
            if not mfa_token:
                return False
                
            # Здесь должна быть проверка MFA токена
            # TODO: Реализовать проверку MFA токена
            return True
            
        return True


def jwt_response_payload_handler(token, user=None, request=None) -> dict:
    """
    Обработчик для формирования ответа с JWT токеном
    """
    return {
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': user.get_role_permissions()
        }
    }
