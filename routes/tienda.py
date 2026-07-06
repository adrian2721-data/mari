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
import os
from whatsapp_api_client_python import API
from dotenv import load_dotenv
load_dotenv()

# Almacenamiento de carritos por sesión (en memoria)
carritos: Dict[str, Carrito] = {}

router = APIRouter(
    prefix="/tienda",  # Todos los endpoints empezarán con /productos
    tags=["Tienda"],  # Para agrupar en la documentación /docs
)

templates = Jinja2Templates(directory="templates")  # directorio de los html
router.mount(
    "/static", StaticFiles(directory="static"), name="static"
    
)  # cargar los css


SessionDep = Annotated[Session, Depends(get_session)]
def get_carrito(request: Request) -> Carrito:
    """Obtiene o crea un carrito para la sesión actual"""
    session_id = request.cookies.get("session_id", "default_session")

    if session_id not in carritos:
        carritos[session_id] = Carrito()

    return carritos[session_id]

@router.get("/todos", response_class=HTMLResponse)
def all_producto(request: Request, session: SessionDep):
    resultado = session.exec(select(Producto)).all()
    if not resultado:
        raise HTTPException(status_code=404, detail="producto not found")
    carrito = get_carrito(request)
    return templates.TemplateResponse(
        request=request,
        name="producto.html",
        context={
            "dato": resultado,
            "carro": jsonable_encoder(carrito.obtener_resumen()),
        },)

@router.get("/items/{id}", response_class=HTMLResponse)
async def get_producto(request: Request, id: str, session: SessionDep):
    resultado = session.exec(select(Producto).where(Producto.name == id)).all()
    if not resultado:
        return templates.TemplateResponse(
            request=request, name="producto.html", context={"existe": True}
        )
    return templates.TemplateResponse(
        request=request,
        name="producto.html",
        context={
            "dato": resultado,
        },
    )


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, session: SessionDep):
    resultado = session.exec(select(Producto)).all()
    carrito = get_carrito(request)
    return templates.TemplateResponse(
        request=request,
        name="catalogo.html",
        context={
            "dato": resultado,
            "carro": jsonable_encoder(carrito.obtener_resumen()),
        },
    )

@router.post("/carrito/agregar/{producto_id}")
async def agregar_al_carrito(
    producto_id: int,
    request: Request = None,
    cantidad: int = 1,
    session: Session = Depends(get_session),
):
    """Agrega un producto al carrito"""

    # Obtener producto de la base de datos
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener carrito de la sesión
    carrito = get_carrito(request)

    # Agregar al carrito
    resultado = carrito.agregar(
        producto_id=producto.id,
        nombre=producto.name,
        precio=Decimal(str(producto.price)),
        cantidad=cantidad,
        imagen=producto.imagen if hasattr(producto, "imagen") else None,
    )

    return JSONResponse(content=jsonable_encoder(resultado))


@router.post("/carrito/eliminar/{producto_id}")
async def eliminar_del_carrito(producto_id: int, request: Request):
    """Elimina un producto del carrito"""
    carrito = get_carrito(request)
    resultado = carrito.eliminar(producto_id)
    resumen = carrito.obtener_resumen()
    return templates.TemplateResponse(
        request=request,
        name="carros.html",
        context={"carrito": resumen, "items": resumen["items"]},
    )


@router.post("/carrito/sumar/{producto_id}")
async def sumar_cantidad(producto_id: int, request: Request):
    """Actualiza la cantidad de un producto"""
    carrito = get_carrito(request)
    carrito.sumar_cantidad(producto_id)
    resumen = carrito.obtener_resumen()
    # return resumen

    return templates.TemplateResponse(
        request=request,
        name="carros.html",
        context={"carrito": resumen, "items": resumen["items"]},
    )


@router.post("/carrito/restar/{producto_id}", response_class=HTMLResponse)
async def restar_cantidad(producto_id: int, request: Request):
    """Actualiza la cantidad de un producto"""
    carrito = get_carrito(request)
    carrito.restar_cantidad(producto_id)
    resumen = carrito.obtener_resumen()

    return templates.TemplateResponse(
        request=request,
        name="carros.html",
        context={"carrito": resumen, "items": resumen["items"]},
    )


@router.post("/carrito/vaciar")
async def vaciar_carrito(request: Request):
    """Vacía el carrito completamente"""
    carrito = get_carrito(request)
    resultado = carrito.vaciar()
    return JSONResponse(content=jsonable_encoder(resultado))


@router.get("/carrito/resumen")
async def resumen_carrito(request: Request):
    """Obtiene el resumen del carrito"""
    carrito = get_carrito(request)
    return JSONResponse(content=jsonable_encoder(carrito.obtener_resumen()))


@router.get("/carrito", response_class=HTMLResponse)
async def ver_carrito(request: Request):
    """Muestra la página del carrito"""
    carrito = get_carrito(request)
    resumen = carrito.obtener_resumen()

    return templates.TemplateResponse(
        request=request,
        name="carro.html",
        context={"carrito": resumen, "items": resumen["items"]},
    )
    
    
@router.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    """Muestra la página de contacto"""
    return templates.TemplateResponse(
        request=request,
        name="contacto.html",
    )
class FormData(BaseModel):
    nombre: str
    telefono: str
    mensaje: str



idInstance=os.getenv('idInstance')
apiTokenInstance=os.getenv('apiTokenInstance')
greenAPI = API.GreenAPI(
    idInstance, apiTokenInstance
)
def whatsapp(telefono,mensaje):
    response=greenAPI.sending.sendMessage(f"53{telefono}@c.us", f"{mensaje}")
    print(response.data)
    return {"message": response.data}
    
    
    
@router.post("/mensaje")
async def mensaje(request: Request,data: Annotated[FormData, Form()], session: SessionDep):
    carrito = get_carrito(request)
    resumen = carrito.obtener_resumen()
    texto=""
    for i in resumen['items']:
        texto+=f"nombre producto:{i.nombre},precio:{i.precio},cantidad:{i.cantidad},subtototal:${i.subtotal}\n"
    texto+=f"total:${resumen['total']}"
    if data.mensaje !="":
        whatsapp(data.telefono,f"Buenas {data.nombre},este es su pedidio:\n{texto}\n mensaje:{data.mensaje}")
    else:
        whatsapp(data.telefono,f"Buenas {data.nombre},este es su pedidio:\n{texto}\n")
    carrito.vaciar()
    carrito = get_carrito(request)
    resultado = session.exec(select(Producto)).all()
    return templates.TemplateResponse(
        request=request,
        name="catalogo.html",
        context={
            "dato": resultado,
            "carro": jsonable_encoder(carrito.obtener_resumen()),
        },
    )