from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Connection(Base):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_gate_id: Mapped[str] = mapped_column(String(10), ForeignKey("gates.gate_id"), nullable=False)
    to_gate_id: Mapped[str] = mapped_column(String(10), ForeignKey("gates.gate_id"), nullable=False)
    distance_hu: Mapped[float] = mapped_column(Float, nullable=False)
