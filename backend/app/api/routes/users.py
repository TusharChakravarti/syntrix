from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.deps import get_db
from app.schemas.user import UserCreate,UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/",response_model=UserResponse)
async def register_user(
    user_data:UserCreate,
    db:AsyncSession = Depends(get_db)


):
    try:
        user = await create_user(
            db = db,
            clerk_user_id=user_data.clerk_user_id,
            email= user_data.email,
            full_name = user_data.full_name
        )

        return user



    except Exception as e:
       await db.rollback()
       print("User CREATION ERROR",repr(e))
       raise HTTPException(
           status_code=500,
           detail="Could not create user"
       )