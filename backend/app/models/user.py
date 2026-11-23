from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization_membership import OrganizationMembership



class User(Base):
    __tablename__= "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    clerk_user_id:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False, 
    
    )
    email:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    full_name:Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    memberships:Mapped[list["OrganizationMembership"]] = relationship(
        back_populates="user"
    )