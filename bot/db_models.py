from datetime import datetime

from sqlalchemy import Column, String, Integer, Table, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(254), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    telegram_id: Mapped[str] = mapped_column(String(60), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_joined: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)


    # Many-to-Many relationship with Discount (set to None for now)
    fav_discounts = []

    def __str__(self):
        return self.username


    
