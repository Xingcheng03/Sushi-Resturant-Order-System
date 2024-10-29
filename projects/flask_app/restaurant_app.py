from flask import Flask, render_template, request, url_for, abort, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Sushi_model import Base_sushi, Sushi
from Main_plate_model import Base_main_plate, Plate
from Order_model import Base_order, Order

app = Flask(__name__)

# Database setup
engine_orders = create_engine('sqlite:///orders.db')
Base_order.metadata.bind = engine_orders
DBSession_order = sessionmaker(bind=engine_orders)
session_orders = DBSession_order()

engine_main_plates = create_engine('sqlite:///main_plates.db')
Base_main_plate.metadata.bind = engine_main_plates
DBSession_main_plate = sessionmaker(bind=engine_main_plates)
session_main_plate = DBSession_main_plate()

engine_sushis = create_engine('sqlite:///sushis.db')
Base_sushi.metadata.bind = engine_sushis
DBSession_sushi = sessionmaker(bind=engine_sushis)
session_sushi = DBSession_sushi()

# Routes

@app.route("/", methods=['GET'])
def welcome_page():
    return render_template('welcome.html', main_menu=url_for('main_menu_page'))

@app.route("/regenerate_database/")
def regenerate_database():
    # Regenerate sushi database
    sushis = [
        Sushi(type="Salmon", image="salmon.jpg", price=5.99),
        Sushi(type="Tuna", image="tuna.jpg", price=6.99),
        Sushi(type="Eel", image="eel.jpg", price=7.99),
        Sushi(type="Crab", image="crab.jpg", price=8.99),
        Sushi(type="Shrimp", image="shrimp.jpg", price=5.49)
    ]
    for sushi in sushis:
        session_sushi.add(sushi)
    session_sushi.commit()
    # Regenerate main_plate database
    plates = [
        Plate(type="Beef", image="beef.jpg", url="beef.html"),
        Plate(type="Chicken", image="chicken.jpg", url="chicken.html"),
        Plate(type="Vegetarian", image="vegetarian.jpg", url="vegetarian.html"),
        Plate(type="Seafood", image="seafood.jpg", url="seafood.html"),
        Plate(type="Pasta", image="pasta.jpg", url="pasta.html")
    ]
    for plate in plates:
        session_main_plate.add(plate)
    session_main_plate.commit()
    return "Databases regenerated!"

@app.route("/main_menu/")
def main_menu_page():
    plates = session_main_plate.query(Plate).all()
    print(plates)
    plates_json = [plate.toJSON() for plate in plates]
    print(plates_json)

    return render_template('main_menu.html', main_plates=plates_json)

@app.route("/sushis/")
def sushi_page():
    sushis = session_sushi.query(Sushi).all()
    sushis_json = [sushi.toJSON() for sushi in sushis]
    return render_template('sushi_menu.html', sushis=sushis_json)

@app.route("/order_request/", methods=["POST"])
def order_request():
    order_requests = request.form['order_summary'].split("\n")
    customer_name = request.form['customer_name']
    new_order = Order(customer_name=customer_name, 
    orders=request.form['order_summary'])
    try:
        session_orders.add(new_order)
        session_orders.commit()
    except:
        session_orders.rollback()
        abort(500)
    return render_template('order_summary.html', order_requests=order_requests, customer_name=customer_name)

@app.route("/kitchen/")
def kitchen():
    orders = session_orders.query(Order).all()
    orders_json = [order.toJSON() for order in orders]
    return render_template('kitchen.html', orders=orders_json)

@app.route("/delete/<int:id>")
def delete(id):
    order = session_orders.query(Order).filter(Order.id == id).first()
    if not order:
        abort(404)
    session_orders.delete(order)
    session_orders.commit()
    return redirect(url_for('kitchen'))

if __name__ == "__main__":
    app.run(debug=True)
