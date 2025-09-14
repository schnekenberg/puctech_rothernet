from sqlalchemy.orm import Session
from models import Client, Order, Dish, OrderItem
from datetime import datetime

#add a new client by cpf and return it
def add_client(db, cpf : str):
    new_client = Client(cpf = cpf)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client

#matches the client using the cpf and returns it 
#Remainder: change the execption behavior
def get_client(db, cpf: str):
    client =  db.query(Client).filter(Client.cpf == cpf).first()
    
    if not client: #the client doesnt exist
        return -1 #This is just an exception handling for now
    return client

def add_order(db, cpf: str, dish_items: list):
    order = Order(client_cpf=cpf, order_time=datetime.utcnow())
    db.add(order)
    db.commit()
    db.refresh(order)
    items = []

    for dish_id, quantity in dish_items:
        item = OrderItem(order_id=order.id, dish_id=dish_id, quantity=quantity)
        items.append(item)
    db.add_all(items)
    db.commit()
    
    return order
def get_order_items(db, order_id: int):
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def get_dish(db: Session, dish_id: int):
    return db.query(Dish).filter(Dish.id == dish_id).first()

def get_all_dishes(db):
    return db.query(Dish).all()

def add_dish(db: Session, name: str, price: int):
    dish = Dish(name=name, price=price)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


def delete_order(db, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        return True
    return False

def delete_client(db, cpf: str):
    client = db.query(Client).filter(Client.cpf == cpf).first()
    if client:
        db.delete(client)
        db.commit()
        return True
    return False

def get_client_orders(db, cpf: str):
    return db.query(Order).filter(Order.client_cpf == cpf).all()
