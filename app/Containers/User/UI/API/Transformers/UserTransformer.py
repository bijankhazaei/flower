from app.Containers.User.Models.User import User

class UserTransformer:
    @staticmethod
    def transform(user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "status": user.status.value,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }