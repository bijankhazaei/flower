from functools import wraps
from fastapi import HTTPException, status
from app.Containers.User.Models.User import User, UserRole


def require_role(*allowed_roles: UserRole):
    """Decorator to require specific user roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user or not isinstance(current_user, User):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_admin(func):
    """Decorator to require admin or super_admin role"""
    return require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN)(func)


def require_super_admin(func):
    """Decorator to require super_admin role"""
    return require_role(UserRole.SUPER_ADMIN)(func)


def can_manage_project(user: User, project_owner_id: str) -> bool:
    """Check if user can manage a specific project"""
    if user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        return True
    return str(user.id) == project_owner_id


def can_access_project(user: User, project_owner_id: str) -> bool:
    """Check if user can access a specific project"""
    # For now, all users can access projects they're assigned to
    # This would be enhanced with UserProject relationships
    return True