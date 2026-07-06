from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from fastapi.encoders import jsonable_encoder
from schemas.producto import *
from model import Producto, Categoria
from bd import get_session
from typing import Dict
from decimal import Decimal
from carro import Carrito
from model import Producto
from bd import get_session
from sqlmodel import Session

# Almacenamiento de carritos por sesión (en memoria)
carritos: Dict[str, Carrito] = {}

router = APIRouter(
    prefix="/producto",  # Todos los endpoints empezarán con /productos
    tags=["Productos"],  # Para agrupar en la documentación /docs
)

templates = Jinja2Templates(directory="templates")  # directorio de los html
router.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # cargar los css


SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/crear")
async def create_producto(
    request: Request,
    session: SessionDep,
    imagen: UploadFile,
    name: str = Form(),
    price: float = Form(),
):
    upload_dir = Path("static/uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = f"{upload_dir}/{imagen.filename}"

    # Guardar el archivo usando write()
    with open(file_path, "wb") as buffer:
        buffer.write(await imagen.read())
    nombre_original = imagen.filename
    # Crear el producto con valores por defecto para categoria y proveedor
    nuevo_producto = Producto(
        name=name,
        price=price,
        imagen=nombre_original,
        # o proveedor_id si se proporcionó
    )

    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)

    # return nuevo_producto
    return templates.TemplateResponse(
        request=request,
        name="productos/producto.html",
        context={"message": "Producto creado exitosamente",}
    )



@router.get("/")
def producto(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request=request,
        name="productos/producto.html",
    )


@router.get("/todos")
def all_producto(request: Request, session: SessionDep):
    resultado = session.exec(select(Producto)).all()
    if not resultado:
        raise HTTPException(status_code=404, detail="producto not found")

    return resultado


@router.patch("/{item_id}", response_model=ProductoPublic)
def update_producto(hero_id: int, hero: ProductoUpdate, session: SessionDep):
    resultado = session.get(Producto, hero_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="producto not found")
    hero_data = hero.model_dump(exclude_unset=True)
    resultado.sqlmodel_update(hero_data)
    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado


@router.delete("/delete/{item_id}")
def delete_producto(item_id: int, session: SessionDep):
    db_hero = session.get(Producto, item_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return {"ok": True, "eliminado": db_hero.name}


@router.get("/items/{id}/{cat}")
async def get_producto(request: Request, id: str, cat: int, session: SessionDep):
    resultado = session.exec(
        select(Producto).where(Producto.name == id, Producto.categoria_id == cat)
    )
    return resultado
