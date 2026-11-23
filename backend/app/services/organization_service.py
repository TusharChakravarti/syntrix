from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership


async def create_organization(
        db:AsyncSession,
        user_id:int,
        name:str,
        slug:str,


)->Organization:
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

