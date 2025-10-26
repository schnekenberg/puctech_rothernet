from servidor.database import SessionLocal, crud
from servidor.database.models import Client, Order, Dish, OrderItem


db = SessionLocal()

#Add clients
# new_client = crud.add_client(db, "11779221")
# new_client = crud.add_client(db, "117792241")
# new_client = crud.add_client(db, "552779221")
# new_client = crud.add_client(db, "1177ee2451")
# print("client added") #I need to create a try and catch in case a client thats already in the db tries to be inserted, cause it raises an ungly error


# new_client = crud.get_client(db, "11779221")

# if new_client == -1:
#     print("Client doesnt exist in the database")
# else:
#     print("Client exists")
 #Delete Client
is_client_deleted = crud.delete_client(db,"11779221")

if is_client_deleted: 
    print("Client has been deleted")
else:
    print("Maybe the client doesnt exist in the db")

#Add a dish
# orders = crud.get_client_orders(db, "124444")

# if not orders:
#     print("There are no orders matched with the given cpf")
# else:
#     print("There are some orders") 

# clients = db.query(Client).all()

# for client in clients:
#      print(f"Client CPF: {client.cpf}")

