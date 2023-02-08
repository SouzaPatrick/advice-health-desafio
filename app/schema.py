from typing import Optional

from flask_marshmallow.fields import fields
from marshmallow import post_load, validates
from marshmallow.exceptions import ValidationError

from app import ma
from app.db_function import add_cars_in_owner, create_owner, get_owner_and_cars
from app.models import Owner
from tools.person_docs_helper import validate_cpf


class OwnerSchema(ma.Schema):
    name: str = fields.Str(required=True)
    cpf: str = fields.Str(required=True)

    class Meta:
        fields = (
            "name",
            "cpf",
        )

    @validates("cpf")
    def validate_document(self, cpf):
        if not validate_cpf(cpf):
            raise ValidationError({"error_message": "Invalid document number"})
        return cpf


class CarSchema(ma.Schema):
    model: str = fields.Str(required=True)
    color: str = fields.Str(required=True)

    class Meta:
        fields = (
            "model",
            "color",
        )

    @validates("color")
    def validate_color(self, color):
        allowed_colors: list = ["yellow", "blue", "gray"]
        if color not in allowed_colors:
            raise ValidationError(
                {
                    "error_message": f"{color} color is invalid, enter a valid color for the car"
                }
            )
        return color

    @validates("model")
    def validate_model(self, model):
        allowed_colors: list = ["hatch", "sedan", "convertible"]
        if model not in allowed_colors:
            raise ValidationError(
                {
                    "error_message": f"{model} model is invalid, enter a valid model for the car"
                }
            )
        return model


class OwnerCarSchema(ma.Schema):
    owner: OwnerSchema = fields.Nested(OwnerSchema, required=True)
    cars: list[CarSchema] = fields.Nested(CarSchema, many=True)

    class Meta:
        fields = (
            "owner",
            "cars",
        )

    @post_load
    def validate(self, data, **kwargs) -> Optional[dict]:
        owner: Owner = get_owner_and_cars(cpf=data.get("owner").get("cpf"))
        if owner is not None:
            if len(owner.cars) == 3:
                raise ValidationError(
                    {
                        "error_message": "The owner already owns the maximum number of cars allowed"
                    }
                )
            elif len(data.get("cars")) + len(owner.cars) > 3:
                raise ValidationError(
                    {
                        "error_message": "The reported amount of cars exceeds the owner's limit"
                    }
                )
        else:
            owner: Owner = create_owner(
                owner=Owner(
                    name=data.get("owner").get("name"), cpf=data.get("owner").get("cpf")
                )
            )

        if len(data.get("cars")) > 3:
            raise ValidationError(
                {"error_message": "The reported number of cars exceeds the limit"}
            )

        add_cars_in_owner(owner_id=owner.id, cars=data.get("cars"))

        return data
