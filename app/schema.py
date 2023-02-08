from typing import List
from app import ma
from flask_marshmallow.fields import fields

class OwnerSchema(ma.Schema):
    name = fields.Str(required=True)
    driver_licence = fields.Str(required=True)

    class Meta:
        fields = (
            "name",
            "driver_licence",
        )


class CarSchema(ma.Schema):
    model = fields.Str(required=True)
    color = fields.Str(required=True)

    class Meta:
        fields = (
            "model",
            "color",
        )

class OwnerCarSchema(ma.Schema):
    owner: OwnerSchema = fields.Nested(OwnerSchema, required=True)
    cars: List[CarSchema] = fields.Nested(CarSchema,  many=True)

    class Meta:
        fields = (
            "owner",
            "cars",
        )