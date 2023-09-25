from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)  # Added unique constraint
    address = db.Column(db.String(255))
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

    @validates('name')
    def validate_name(self, key, name):
        if len(name) > 50:
            raise ValueError('Name must be less than 50 characters.')
        return name

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    ingredients = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    pizza_restaurants = db.relationship('RestaurantPizza', back_populates='pizza')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    price = db.Column(db.Float)

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='pizza_restaurants')
    
    def serialize(self):
        return self.pizza.serialize()

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError('Price must be between 1 and 30.')
        return price
