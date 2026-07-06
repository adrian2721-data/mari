from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from schemas.proveedor import ProveedorCrear,Proveedores,ProveedorUpdate
from model import Proveedor
from bd import get_session

router = APIRouter(
    prefix="/proveedor",  # Todos los endpoints empezarán con /productos
    tags=["Proveedores"]     # Para agrupar en la documentación /docs
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post('/crear')
def ccreate_proveedor(session: SessionDep,item:ProveedorCrear)->Proveedores:
    consulta = Proveedor.model_validate(item)
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta

@router.get('/todos')
def all_proveedor(session: SessionDep)->list[Proveedores]:
    resultado=session.exec(select(Proveedor)).all()
    if not resultado:
        raise HTTPException(status_code=404, detail="proveedor not found")
    return resultado

@router.patch("/{item_id}", response_model=Proveedores)
def update_proveedor(hero_id: int, hero: ProveedorUpdate,session: SessionDep):
    resultado = session.get(Proveedor, hero_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="proveedor not found")
    hero_data = hero.model_dump(exclude_unset=True)
    resultado.sqlmodel_update(hero_data)
    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado

@router.delete("/delete/{item_id}")
def delete_proveedor(item_id: int,session: SessionDep):
    db_hero = session.get(Proveedor, item_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return {'ok':True,'eliminado':db_hero.name}