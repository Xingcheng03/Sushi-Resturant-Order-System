from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
db = SQLAlchemy(app)

# Import your models
from order_model import Base_order, Order
from main_plate_model import Base_main_plate, Plate
from sushi_model import Base_sushi, Sushi

# Bind your models to the SQLAlchemy db instance
Base_order.metadata.create_all(bind=db.engine)
Base_main_plate.metadata.create_all(bind=db.engine)
Base_sushi.metadata.create_all(bind=db.engine)

@app.route('/orders')
def get_orders():
    orders = Order.query.all()
    return jsonify([order.toJSON() for order in orders])

@app.route('/plates')
def get_plates():
    plates = Plate.query.all()
    return jsonify([plate.toJSON() for plate in plates])

@app.route('/sushis')
def get_sushis():
    sushis = Sushi.query.all()
    return jsonify([sushi.toJSON() for sushi in sushis])

if __name__ == '__main__':
    app.run(debug=True)
