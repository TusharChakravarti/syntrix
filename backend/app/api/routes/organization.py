from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.organization import OrganizationCreate,OrganizationResponse
from app.services.organization_service import (
    create_organization,
    get_organization,
    get_user_organizations
    )

router = APIRouter(prefix="/organizations",tags=["Organizations"])
# create organization
@router.post("/",response_model=OrganizationResponse)
async def register_organization(
      organization_data:OrganizationCreate,
      user_id:int,
      db:AsyncSession = Depends(get_db)
):
    try:
        organization = await create_organization(
                   db = db,
                    user_id=user_id,
                    name=organization_data.name,
                    slug=organization_data.slug
            

        )
        return organization
    except Exception as e:
        await db.rollback()
        print("Organization creation Error:",repr(e))
        raise HTTPException(
            status_code=500,
             detail="Could not create organization",
        )


# get all the organization user belongs to

@router.get("/user/{user_id}",response_model=list[OrganizationResponse])
async def list_user_organizations(
    user_id:int,
    db:AsyncSession = Depends(get_db),
):
    return await get_user_organizations(db,user_id)
# get details of the organization through id 
@router.get("/{organiation_id}",response_model=OrganizationResponse)
async def get_organization_details(
    organization_id:int,
    db:AsyncSession = Depends(get_db),
):
    organization = await get_organization(db,organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    return organization

