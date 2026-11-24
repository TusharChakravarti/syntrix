from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserUpdate
async def create_user(
        db:AsyncSession,
        clerk_user_id:str,
        email:str,
        full_name:str | None = None
)->User:
    try:
        user = User(
            clerk_user_id = clerk_user_id,
            email = email,
            full_name = full_name

        )

        db.add(user)
        await db.commit()
        
        return user
    except Exception:
        await db.rollback()
        raise


async def get_user(
        db:AsyncSession,
        user_id:int
)->User | None:
    return await db.get(User,user_id)



async def update_user(
        db:AsyncSession,
        user_id:int,
        updated_data:UserUpdate
):
    user = await db.get(User,user_id)

    if not user:
        return None


    try:
        for key,value in updated_data.model_dump(exclude_unset=True).items():
            setattr(user,key,value)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        raise

async def delete_user(
        db:AsyncSession,
        user_id:int
):
    
    user = await db.get(User,user_id)

    if not user:
        return False

    try:
        await db.delete(user)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise