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

def get_user_by_username(username: str) -> bool:
    with Session() as session:
        user = session.query(User).filter(User.username == username).first()

    return user is not None