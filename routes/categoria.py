from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from schemas.categoria import CategoriaCrear,CategoriaDelete,CategoriaUpdate,Categorias
from model import Categoria
from bd import get_session

router = APIRouter(
    prefix="/categoria",  # Todos los endpoints empezarán con /productos
    tags=["Categorias"]     # Para agrupar en la documentación /docs
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post('/categoria/crear')
def crearCategoria(session: SessionDep,item:CategoriaCrear)->CategoriaCrear:
    db_hero = Categoria.model_validate(item)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get('/categoria/todos')
def crearCategoria(session: SessionDep)->list[Categorias]:
    resultado=session.exec(select(Categoria)).all()
    return resultado

@router.patch("/categoria/{item_id}", response_model=Categorias)
def update_hero(hero_id: int, hero: CategoriaUpdate,session: SessionDep):
    db_hero = session.get(Categoria, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# @router.delete("/categoriaD/{item_id}", response_model=Categorias)
@router.delete("/categoriaD/{item_id}")
def delete_categoria(item_id: int,session: SessionDep):
    db_hero = session.get(Categoria, item_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    # return db_hero
    return {'ok':True,'categorai':db_hero.name}
