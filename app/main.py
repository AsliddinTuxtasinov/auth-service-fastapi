from typing import Union
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get(path="/", status_code=status.HTTP_200_OK)
async def read_root():
    return {
        "success": True,
        "message": "Hello World!"
    }


@app.get(path="/detail/{item_id}", status_code=status.HTTP_200_OK)
async def read_user(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.patch(path="/update/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id: int, item: Item):

    data = item.dict()
    data.update({"item_id": item_id})
    return {
        "success": True,
        "data": data,
    }
