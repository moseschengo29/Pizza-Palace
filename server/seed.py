from app import app
from models import db, Pizza, Restaurant, RestaurantPizza



with app.app_context():
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    
    new_restaurant = Restaurant(name="Restaurant A", address="123 Main St")
    new_pizza = Pizza(name="Pizza 1", ingredients="Tomato, Cheese, Pepperoni")
    new_restaurant_pizza = RestaurantPizza(pizza=new_pizza, restaurant=new_restaurant, price=12.99)

    db.session.add_all([new_restaurant, new_pizza, new_restaurant_pizza])
    db.session.commit()
    