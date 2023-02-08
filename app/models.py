from typing import Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String
from werkzeug.security import check_password_hash, generate_password_hash


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String, unique=True))
    password_hash: str

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cpf: str

    cars: list["Car"] = Relationship(back_populates="owner")


class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str
    color: str

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    owner: Optional[Owner] = Relationship(back_populates="cars")
