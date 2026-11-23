from datetime import datetime

from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import TYPE_CHECKING
from app.models.base import Base
if TYPE_CHECKING:
    from app.models.organization_membership import OrganizationMembership
    from app.models.repository import Repository



class Organization(Base):
    __tablename__ = "organizations"

    id:Mapped[int] = mapped_column(
      primary_key=True
    )
    name:Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    slug:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False

    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    memberships: Mapped[list["OrganizationMembership"]] = relationship(
        back_populates="organization"
    )
  # one org can have many memebers
    repositories:Mapped[list["Repository"]]  = relationship(
        back_populates="organization"
    )

# one org can have many repo
