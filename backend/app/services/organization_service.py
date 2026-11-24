from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
from app.schemas.organization import OrganizationUpdate

async def create_organization(
        db:AsyncSession,
        user_id:int,
        name:str,
        slug:str,


)->Organization:
    try:
        organization = Organization(
            name=name,
            slug = slug
        )

        db.add(organization)


        membership = OrganizationMembership(
        user_id =user_id,
        organization=organization,
        role = "owner"


        )

        db.add(membership)
        await db.commit()
        await db.refresh(organization)

        return organization
    except Exception:
       await db.rollback()
       raise



async def get_user_organizations(
        db:AsyncSession,
        user_id:int
):
 results = await db.execute(
    select(Organization)
    .join(OrganizationMembership)
    .where(OrganizationMembership.user_id == user_id)
 )

 return results.scalars().all()

async def get_organization(
      db:AsyncSession,
      organization_id:int
):
   return await db.get(Organization,organization_id)

async def update_organization(
      db:AsyncSession,
      organization_id:int,
      update_data:OrganizationUpdate
):
   organization = await db.get(Organization,organization_id)
   if not organization:
      return None

   try:

    for key,value in update_data.model_dump(exclude_unset=True).items():
        setattr(organization,key,value)
        


    await db.commit()
    await db.refresh(organization)

    return organization
   except Exception:
      await db.rollback()
      raise




async def delete_organization(
      db:AsyncSession,
      organziation_id:int
):
   
   organization = await db.get(Organization,organziation_id)

   if not organization:
      return False

   try:
   
        await db.delete(organization)
        await db.commit()

        return True
   except Exception:
      await db.rollback()
      raise
    