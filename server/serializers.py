# serializers.py
from marshmallow import fields, Schema
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class SerializerMixin:
    def serialize(self):
        return ma.dump(self)

    def to_dict(self):
        return self.serialize()

class RestaurantSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'address')

class PizzaSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'ingredients', 'created_at', 'updated_at')

class RestaurantPizzaSchema(Schema):
    class Meta:
        fields = ('id', 'restaurant_id', 'pizza_id', 'price', 'created_at', 'updated_at')
