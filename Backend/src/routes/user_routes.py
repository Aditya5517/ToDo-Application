from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from src.database.connection import (
    get_db
)

from src.db_models.auth import User

from src.dependencies.auth_dependencies import (
    require_admin
)

from src.repositories.user_repository import (
    get_all_users
)

from src.schemas.user_schema import (
    UserResponse
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),

    _admin: User = Depends(
        require_admin
    )
):

    return get_all_users(db)