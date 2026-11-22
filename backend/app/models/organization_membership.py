from sqlalchemy import String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column

from app.models.base import Base


class  OrganizationMembership(Base):
    __tablename__ = "organization_membership"

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