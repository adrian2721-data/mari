from pydantic import BaseModel
from sqlmodel import SQLModel

class Categorias(SQLModel):
    id: int
    name: str
class CategoriaCrear(SQLModel):
    name: str
class CategoriaDelete(SQLModel):
    id: int
class CategoriaUpdate(SQLModel):
    name: str | None = None