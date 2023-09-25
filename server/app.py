from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource


from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
    
        return jsonify([restaurant.serialize() for restaurant in restaurants])
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        
        restaurant = Restaurant(name=name, address=address)
        db.session.add(restaurant)
        db.session.commit()
        
        return jsonify(restaurant.serialize()), 201
    
api.add_resource(Restaurants, '/restaurants')    

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify(restaurant.serialize())
        else:
            return jsonify({'error': 'Restaurant not found'}), 404
        
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
    
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'error': 'Restaurant not found'}), 404
    
api.add_resource(RestaurantByID, '/restaurants/<int:id>')

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.serialize())
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.serialize() for pizza in pizzas])
    
api.add_resource(Pizzas, '/pizzas')  

       
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not (1 <= price <= 30):
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

