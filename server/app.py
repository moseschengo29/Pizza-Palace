from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)



# Define routes
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    
    return jsonify([restaurant.serialize() for restaurant in restaurants])

@app.route('/restaurants', methods=['POST'])
def add_restaurant():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    
    restaurant = Restaurant(name=name, address=address)
    db.session.add(restaurant)
    db.session.commit()
    
    return jsonify(restaurant.serialize()), 201
    

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.serialize())
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.serialize() for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not (1 <= price <= 3000):
        return jsonify({'errors': ['Invalid price. Price must be between 1 and 30']}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    try:
        restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(pizza.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['RestaurantPizza already exists']}), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)

