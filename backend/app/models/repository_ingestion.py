from datetime import datetime

from sqlalchemy import String,DateTime,ForeignKey,Text,func
from  sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.repository import Repository



class RepositoryIngestion(Base):
    __tablename__ = "repository_ingestions"

    id:Mapped[int] = mapped_column(primary_key=True)

    repository_id:Mapped[int] = mapped_column(
        ForeignKey("repositories.id",ondelete= "CASCADE"),
        nullable=False
    )
    status:Mapped[str]= mapped_column(
        String(50),
        nullable="False",
        default="pending"

    )
    started_at:Mapped[datetime | None] = mapped_column(
      DateTime(timezone=True),
      nullable=True  
    )
    completed_at:Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    error_message:Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    repository:Mapped["Repository"] = relationship(
        back_populates="ingestions"
    )