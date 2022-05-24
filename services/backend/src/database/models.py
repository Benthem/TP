from sqlalchemy import Column
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy import Table, MetaData
from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy_views import CreateView, DropView

from .database import Base

class Fruit(Base):
    __tablename__ = "fruit"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    color = Column(String(20))
    sales = relationship(
        "Sale", back_populates="fruit", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"Fruit(id={self.id!r}, name={self.name!r}, color={self.color!r})"

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    fruit_id = Column(Integer, ForeignKey("fruit.id"))
    fruit = relationship("Fruit", back_populates="sales")
    amount = Column(Integer)
    CheckConstraint(amount > 0)
    sale_date = Column(DateTime(), default=datetime.datetime.now)
    
    def __repr__(self):
        return f"Sale(id={self.id!r}, email_address={self.email_address!r})"
    
async def build_view(session): 
    definition = text('CREATE VIEW my_view AS SELECT f.color, s.id, s.amount FROM fruit as f JOIN sales as s ON f.id = s.fruit_id')
    await session.execute(definition)
    
async def drop_view(session):
    definition = text('DROP VIEW my_view')
    await session.execute(definition)