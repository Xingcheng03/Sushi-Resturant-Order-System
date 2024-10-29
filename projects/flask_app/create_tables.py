# create_tables.py
from sqlalchemy import create_engine
from Sushi_model import Base_sushi
from Main_plate_model import Base_main_plate
from Order_model import Base_order

engine_orders = create_engine('sqlite:///orders.db')
Base_order.metadata.create_all(engine_orders)

engine_main_plates = create_engine('sqlite:///main_plates.db')
Base_main_plate.metadata.create_all(engine_main_plates)

engine_sushis = create_engine('sqlite:///sushis.db')
Base_sushi.metadata.create_all(engine_sushis)
