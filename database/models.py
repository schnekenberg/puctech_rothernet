from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
# from database import Base  
from .session import Base

class Client(Base):
    __tablename__ = "clients"

    cpf = Column(String(11), primary_key=True)
    orders = relationship("Order", back_populates="client")


class Dish(Base):
    __tablename__ = "pratos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)
    categoria = Column(String(50), nullable=True)


    items = relationship("OrderItem", back_populates="dish")

class Order(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_cpf = Column(String(11), ForeignKey("clients.cpf"))
    data_pedido = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pendente")  # pendente, em preparação, entregue

    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    prato_id = Column(Integer, ForeignKey("pratos.id"))
    quantidade = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    dish = relationship("Dish", back_populates="items")
