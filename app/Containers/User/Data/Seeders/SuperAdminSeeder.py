from app.Containers.User.Models.User import User, UserRole, UserStatus
from app.Containers.User.Data.Repositories.UserRepository import UserRepository
from passlib.context import CryptContext

class SuperAdminSeeder:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repository = UserRepository()

    def run(self):
        # Check if super admin already exists
        existing_admin = self.user_repository.find_by_email("admin@flower.com")
        if existing_admin:
            print("Super admin already exists")
            return existing_admin

        # Create super admin user
        admin_data = {
            "name": "Super Admin",
            "email": "admin@flower.com",
            "password_hash": self.pwd_context.hash("admin123"),
            "role": UserRole.SUPER_ADMIN,
            "status": UserStatus.ACTIVE
        }

        admin_user = self.user_repository.create(admin_data)
        print(f"Super admin created: {admin_user.email}")
        return admin_user