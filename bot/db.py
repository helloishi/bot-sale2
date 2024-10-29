from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

from config import db_config
from db_models import User

user = db_config.db_user
password = db_config.db_pass.get_secret_value()
host = db_config.db_host
port = db_config.db_port
database = db_config.db_name

engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_user_by_username(username: str) -> Optional[User]:
    with Session() as session:
        user = session.query(User).filter(User.username == username).first()
    
    print(user.name)

    return user or None

def create_user(username: str, name: Optional[str] = None, telegram_id: Optional[str] = None) -> User:
    with Session() as session:
        new_user = User(
            username=username,
            name=name,
            telegram_id=telegram_id,
            password="000000",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            first_name=name,
            last_name='',
            email='',
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user