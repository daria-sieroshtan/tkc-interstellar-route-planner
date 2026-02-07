from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Gate(Base):
    __tablename__ = "gates"

    gate_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    gate_name: Mapped[str] = mapped_column(String(50), nullable=False)
