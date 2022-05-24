from typing import List, Tuple

from sqlalchemy import func, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from asyncpg.exceptions import CheckViolationError

from .models import Fruit, Sale

class FruitDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def create_fruit(self, name: str, color:str):
        new_fruit = Fruit(name=name, color=color)
        self.db_session.add(new_fruit)
        await self.db_session.flush()
        
    async def get_all_fruits(self) -> List[Fruit]:
        q = await self.db_session.execute(select(Fruit).order_by(Fruit.id))
        return q.scalars().all()
    
class SaleDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def create_sale(self, fruit: str, amount: int):
        q = await self.db_session.execute(select(Fruit).where(Fruit.name == fruit))
        if not q:
            return
        
        new_sale = Sale(fruit=q.scalar(), amount=amount)
        self.db_session.add(new_sale)
        await self.db_session.flush()
        
    async def get_all_sales(self) -> List[Sale]:
        q = await self.db_session.execute(select(Sale).order_by(Sale.id))
        return q.scalars().all()
    
class ViewDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def get_totals(self) -> List[Tuple]:
        q = await self.db_session.execute(text('SELECT color, SUM(amount) FROM my_view GROUP BY color '))
        return q.all()