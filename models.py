from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float
from datetime import date
from database import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    salary_increase_date: Mapped[date|None] = mapped_column(nullable=True)
