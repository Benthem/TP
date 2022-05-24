from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from src.database.database import engine, Base, async_session
from src.database.dals import FruitDAL, SaleDAL, ViewDAL
from src.database.models import Fruit, Sale, build_view, drop_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def fill_db():
    fruit_data = [
        ('orange', 'orange'),
        ('papaya', 'orange'),
        ('strawberry', 'red'),
        ('lime', 'green'),
        ('pear', 'green'),
    ]

    sale_data = [
        ('orange', 120),
    #    ('orange', -5),
        ('lime', 1212121),
        ('papaya', 3)
    ]
    
    async with async_session() as session:
        async with session.begin():
            fruit_dal = FruitDAL(session)
            for fruit in fruit_data:
                await fruit_dal.create_fruit(*fruit)
            
            sale_dal = SaleDAL(session)
            for sale in sale_data:
                await sale_dal.create_sale(*sale)

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await drop_view(conn)
        await conn.run_sync(Base.metadata.reflect)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await build_view(conn)
    await fill_db()

@app.get("/")
async def home():
    async with async_session() as session:
        async with session.begin():
            view_dal = ViewDAL(session)
            return await view_dal.get_totals()

@app.post("/fruit")
async def create_fruit(name: str, color: str):
    async with async_session() as session:
        async with session.begin():
            fruit_dal = FruitDAL(session)
            return await fruit_dal.create_fruit(name, color)

@app.get("/fruit")
async def get_all_fruit() -> List[Fruit]:
    async with async_session() as session:
        async with session.begin():
            fruit_dal = FruitDAL(session)
            return await fruit_dal.get_all_fruits()

@app.post("/sales")
async def create_sale(fruit: str, amount: int):
    try:
        async with async_session() as session:
            async with session.begin():
                sale_dal = SaleDAL(session)
                return await sale_dal.create_sale(fruit, amount)
    except:
        return "Negative sales are not allowed"

@app.get("/sales")
async def get_all_sales() -> List[Sale]:
    async with async_session() as session:
        async with session.begin():
            sale_dal = SaleDAL(session)
            return await sale_dal.get_all_sales()