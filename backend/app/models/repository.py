from datetime import datetime

from sqlalchemy import String,DateTime,ForeignKey,func
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.repository_ingestion import RepositoryIngestion
    from app.models.organization import Organization

class Repository(Base):
    __tablename__ = "repositories"

    id:Mapped[int] = mapped_column(primary_key=True)

    organization_id:Mapped[int] = mapped_column(
        ForeignKey("organizations.id",ondelete="CASCADE"),
        nullable=False
    )
    github_repo_id:Mapped[int] = mapped_column(
      unique=True,
      nullable=False
    )
    name:Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    full_name:Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    html_url:Mapped[str] = mapped_column(
    String(1000),
    nullable=False
    )
    clone_url:Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    default_branch:Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="main"
    )

    is_private:Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    organization:Mapped["Organization"] = relationship(
        back_populates="repositories"
    )
    ingestions:Mapped[list["RepositoryIngestion"]] = relationship(
        back_populates="repository"
    )