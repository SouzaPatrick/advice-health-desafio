from flask import current_app
from sqlmodel import Session, select

from .models import User


def get_user_by_username(username) -> User:
    query = select(User).where(User.username == username)

    with Session(current_app.engine) as session:
        result = session.execute(query).scalars().one()

    return result

def create_user_test():
    user: User = User(username="advicehealth", send_cashback=True)
    user.generate_password("advicehealth")

    with Session(current_app.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)