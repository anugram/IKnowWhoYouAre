from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import get_password_hash

class UserService:

    @staticmethod
    def create_user(user_data: UserCreate) -> UserResponse:
        hashed_password = get_password_hash(user_data.password)
        user = UserRepository.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        return UserResponse.from_orm(user)

    @staticmethod
    def get_user(user_id: str) -> UserResponse:
        user = UserRepository.get_user_by_id(user_id)
        if user:
            return UserResponse.from_orm(user)
        return None

    @staticmethod
    def update_user(user_id: str, user_data: UserCreate) -> UserResponse:
        hashed_password = get_password_hash(user_data.password)
        updated_user = UserRepository.update_user(
            user_id=user_id,
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        if updated_user:
            return UserResponse.from_orm(updated_user)
        return None
