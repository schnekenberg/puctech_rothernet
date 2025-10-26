from servidor.database import SessionLocal, crud, engine, Base
from servidor.database.models import Client, Order, Dish, OrderItem

# This will create all tables in your Supabase database
#disclaimer: don't run this script because the tables have already been created on supabase
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
