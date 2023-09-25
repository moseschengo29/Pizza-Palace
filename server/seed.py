from app import app
from models import db, Pizza, Restaurant, RestaurantPizza



with app.app_context():
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    
    restaurant1 = Restaurant(name='Pizza Palace', address='123 Main St')
    restaurant2 = Restaurant(name='Italian Bistro', address='456 Elm St')
    restaurant3 = Restaurant(name='Pasta House', address='789 Oak St')

    # Add the restaurants to the session and commit
    db.session.add_all([restaurant1, restaurant2, restaurant3])
    db.session.commit()

    # Create data for the Pizza table
    pizza1 = Pizza(name='Margherita', ingredients='Tomato sauce, mozzarella, basil')
    pizza2 = Pizza(name='Pepperoni', ingredients='Tomato sauce, mozzarella, pepperoni')
    pizza3 = Pizza(name='Vegetarian', ingredients='Tomato sauce, mozzarella, bell peppers, onions, mushrooms')

    db.session.add_all([pizza1, pizza2, pizza3])
    db.session.commit()

    # Create data for the RestaurantPizza table
    restaurant_pizza1 = RestaurantPizza(price=10.99, restaurant=restaurant1, pizza=pizza1)
    restaurant_pizza2 = RestaurantPizza(price=12.99, restaurant=restaurant1, pizza=pizza2)
    restaurant_pizza3 = RestaurantPizza(price=11.99, restaurant=restaurant2, pizza=pizza2)
    restaurant_pizza4 = RestaurantPizza(price=14.99, restaurant=restaurant2, pizza=pizza3)

    db.session.add_all([restaurant_pizza1, restaurant_pizza2, restaurant_pizza3, restaurant_pizza4])
    db.session.commit()
    