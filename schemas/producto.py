from fastapi import UploadFile
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Productos(SQLModel):
    id: int
    name: str
    price: float
    active: bool
    description: str
    categoria_id:int
    proveedor_id:int
class ProductoPublic(SQLModel):
    name: str
    price: float
    active: bool
    description: str
    categoria_id:int
    proveedor_id:int
class ProductoUpdate(SQLModel):
    price: float | None=1.0
    active: bool
    description: str | None=None
    categoria_id:int=Field(default=None)
    proveedor_id:int=Field(default=None)