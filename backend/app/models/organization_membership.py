from sqlalchemy import String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class  OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            name="uq_user_organization"
        ),
    )

    id:Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False
    )
    organization_id:Mapped[int] =mapped_column(
        ForeignKey("organizations.id",ondelete="CASCADE"),
        nullable=False
    )
    role:Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="developer"
    )

    user:Mapped["User"] = relationship(
        back_populates="memberships"
    )
    organization:Mapped["Organization"] = relationship(
        back_populates="memberships"
    )