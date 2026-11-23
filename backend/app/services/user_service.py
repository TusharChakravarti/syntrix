from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def create_user(
        db:AsyncSession,
        clerk_user_id:str,
        email:str,
        full_name:str | None = None
)->User:
    user = User(
        clerk_user_id = clerk_user_id,
        email = email,
        full_name = full_name

    )

    db.add(user)
    await db.commit()

    return user



