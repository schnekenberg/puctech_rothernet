from database import SessionLocal, crud
from database.models import Client, Order, Dish, OrderItem


db = SessionLocal()

#Add client
# new_clieadd_client(db, "11779221")
# print("client added")nt = crud.

#Delete Client
# is_client_deleted = crud.delete_client(db,"11779221")

# if is_client_deleted: 
#     print("Client has been deleted")
# else:
#     print("Maybe the client doesnt exist in the db")

#Add a dish
# orders = crud.get_client_orders(db, "124444")

# if not orders:
#     print("There are no orders matched with the given cpf")
# else:
#     print("There are some orders") 
