from flask_marshmallow.fields import fields
from marshmallow import validates
from marshmallow.exceptions import ValidationError

from app import ma
from tools.person_docs_helper import validate_cpf


class OwnerSchema(ma.Schema):
    name = fields.Str(required=True)
    cpf = fields.Str(required=True)

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
    model = fields.Str(required=True)
    color = fields.Str(required=True)

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
