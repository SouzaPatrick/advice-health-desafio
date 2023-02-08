from flask import current_app
from sqlmodel import Session, select
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
from .models import User


def get_user_by_username(username) -> Optional[User]:
    query = select(User).where(User.username == username)

    try:
        with Session(current_app.engine) as session:
            result: Optional[User] = session.execute(query).scalars().one()
    except NoResultFound:
        result: Optional[User] = None

    return result

def create_user_test():
    user: User = User(username="advicehealth", send_cashback=True)
    user.generate_password("advicehealth")

    with Session(current_app.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)