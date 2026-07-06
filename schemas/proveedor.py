from pydantic import BaseModel
from sqlmodel import SQLModel

class Proveedores(SQLModel):
    id: int
    name: str
    phone: str 
class ProveedorCrear(SQLModel):
    name: str
    phone: str 
class ProveedorUpdate(SQLModel):
    name: str
    phone: str