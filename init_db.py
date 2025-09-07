from database import engine, Base
from models import Client, Dish, Order, OrderItem

# This will create all tables in your Supabase database
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
