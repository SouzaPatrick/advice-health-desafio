from typing import NoReturn, Optional

from flask import current_app
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from .models import Car, Owner, User


def get_user_by_username(username) -> Optional[User]:
    query = select(User).where(User.username == username)

    try:
        with Session(current_app.engine) as session:
            result: Optional[User] = session.execute(query).scalars().one()
    except NoResultFound:
        result: Optional[User] = None

    return result


def create_user_test() -> NoReturn:
    user: User = User(username="advicehealth")
    user.generate_password("advicehealth")

    with Session(current_app.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)


def get_owner_and_cars(cpf: str) -> Optional[Owner]:
    query = select(Owner).where(Owner.cpf == cpf).options(joinedload("cars"))
    try:
        with Session(current_app.engine) as session:
            result: Optional[Owner] = session.execute(query).scalars().unique().one()
    except NoResultFound:
        result: Optional[Owner] = None

    return result


def add_cars_in_owner(owner_id: int, cars: list[dict]) -> NoReturn:
    for car in cars:
        car: Car = Car(
            model=car.get("model"), color=car.get("color"), owner_id=owner_id
        )
        with Session(current_app.engine) as session:
            session.add(car)
            session.commit()


def create_owner(owner: Owner) -> Owner:
    with Session(current_app.engine) as session:
        session.add(owner)
        session.commit()
        session.refresh(owner)
    return owner
