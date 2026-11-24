from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.deps import get_db
from app.schemas.user import UserCreate,UserResponse,UserUpdate
from app.services.user_service import (create_user,get_user,update_user,delete_user)


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


# get the user_    
@router.get("/{user_id}",response_model=UserResponse)
async def get_user_details(
    user_id:int,
    db:AsyncSession = Depends(get_db)
):
    user = await get_user(db,user_id)

    if not user:
       raise HTTPException(
           status_code=404,
           detail="User not found"
       )
    return user

@router.patch("/{user_id}",response_model=UserResponse)
async def update_user_details(
    user_id:int,
    user_data:UserUpdate,
    db:AsyncSession = Depends(get_db)
):
    user = await update_user(db,user_id,user_data)
    if not user:
        raise HTTPException(
            status_code=404,
            detail = "User not found"
        )
    return user


@router.delete("/{user_id}")
async def delete_user_details(
    user_id:int,
    db:AsyncSession = Depends(get_db)
):
    deleted =  await delete_user(db,user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {"message":"User deleted successfully"}
