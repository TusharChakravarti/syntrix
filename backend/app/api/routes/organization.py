from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.organization import OrganizationCreate,OrganizationResponse,OrganizationUpdate
from sqlalchemy.exc import IntegrityError

from app.services.organization_service import (
    create_organization,
    get_organization,
    get_user_organizations,
    update_organization,
    delete_organization
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

        return await create_organization(
                   db = db,
                    user_id=user_id,
                    name=organization_data.name,
                    slug=organization_data.slug
            

        )
    except IntegrityError as e:
        error_message = str(e.orig)
        if "organizations_slug_key" in error_message:
              raise HTTPException(
                status_code=409,
                detail="Organization slug already exists",
            )

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
@router.get("/{organization_id}",response_model=OrganizationResponse)
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


@router.patch("/{organization_id}",response_model=OrganizationResponse)
async def update_organization_details(
    organization_id:int,
    organization_data:OrganizationUpdate,
    db:AsyncSession = Depends(get_db),

):
    try:
        organization = await update_organization(
            db,
            organization_id,
            organization_data
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail = "Organization not found",
            )

        return organization
    except IntegrityError as e:
        error_message = str(e.orig)

        if "organizations_slug_key" in error_message:
                raise HTTPException(
                    status_code=409,
                    detail="Organization slug already exists",
                )
        raise HTTPException(
                status_code=500,
                detail="Could not update organization",
            )
        


@router.delete("/{organization_id}")
async def delete_organization_details(
    organization_id:int,
    db:AsyncSession = Depends(get_db)
):
    deleted = await delete_organization(db,organization_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail ="Organization not found"
        )

    
    return {"message": "Organization deleted successfully"}
