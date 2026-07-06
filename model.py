# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from bd import Base
from sqlmodel import Field, Relationship, SQLModel

class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"
    id: int | None = Field(default=None, primary_key=True)
    name: str=Field(max_length=100)
    productos: list["Producto"] = Relationship(back_populates="categoria")
    
class Proveedor(SQLModel, table=True):
    __tablename__ = "proveedor"
    id: int | None = Field(default=None, primary_key=True)
    name: str=Field(max_length=100)
    phone: str = Field(max_length=15)
    productos: list["Producto"] = Relationship(back_populates="proveedor")
    
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str=Field(max_length=100)
    price: float = Field(gt=0)  # decimal_places no es válido
    active: bool = Field(default=True)  # Cambié 'descr' por 'active'
    description: str | None
    imagen: str | None
    categoria_id:int | None=Field(default=None,foreign_key="categoria.id")
    categoria: Categoria | None = Relationship(back_populates="productos")
    proveedor_id:int | None=Field(default=None,foreign_key="proveedor.id")
    proveedor: Proveedor | None = Relationship(back_populates="productos")