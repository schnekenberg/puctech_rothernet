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

ß
