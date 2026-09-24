from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select

from models import Item
from schemas import ItemCreate, ItemRead


app = FastAPI(title="College Lost & Found API")


DATABASE_URL = "sqlite:///lost_found.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate):
    with Session(engine) as session:
        db_item = Item(**item.model_dump())

        session.add(db_item)
        session.commit()
        session.refresh(db_item)

        return db_item


@app.get("/items", response_model=list[ItemRead])
def get_items():
    with Session(engine) as session:
        statement = select(Item)

        items = session.exec(statement).all()

        return items


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    updated_item: ItemCreate
):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        item.title = updated_item.title
        item.description = updated_item.description
        item.category = updated_item.category
        item.location = updated_item.location
        item.reported_by = updated_item.reported_by
        item.status = updated_item.status

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {
            "message": "Item deleted successfully"
        }