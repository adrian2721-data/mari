# carrito.py
from typing import Dict, List, Optional
from pydantic import BaseModel
from decimal import Decimal

class ItemCarrito(BaseModel):
    producto_id: int
    nombre: str
    precio: Decimal
    cantidad: int
    subtotal: Decimal
    imagen: Optional[str] = None

class Carrito:
    def __init__(self):
        # Diccionario principal: {producto_id: ItemCarrito}
        self.items: Dict[int, ItemCarrito] = {}
        self.total: Decimal = Decimal('0.00')
        self.total_items: int = 0
    
    def agregar(self, producto_id: int, nombre: str, precio: Decimal, 
                cantidad: int = 1, imagen: Optional[str] = None) -> Dict:
        """Agrega un producto al carrito"""
        
        if producto_id in self.items:
            # Si ya existe, actualizar cantidad
            item = self.items[producto_id]
            item.cantidad += cantidad
            item.subtotal = item.precio * item.cantidad
        else:
            # Si es nuevo, crear item
            item = ItemCarrito(
                producto_id=producto_id,
                nombre=nombre,
                precio=precio,
                cantidad=cantidad,
                subtotal=precio * cantidad,
                imagen=imagen
            )
            self.items[producto_id] = item
        
        self._actualizar_totales()
        return self.obtener_resumen()
    
    def eliminar(self, producto_id: int) -> Dict:
        """Elimina un producto del carrito"""
        if producto_id in self.items:
            del self.items[producto_id]
            self._actualizar_totales()
        return self.obtener_resumen()
    
    def sumar_cantidad(self, producto_id: int) -> Dict:
        """Actualiza la cantidad de un producto"""
        if producto_id in self.items:
            item = self.items[producto_id]
            item.cantidad += 1
            item.subtotal = item.precio * item.cantidad
            self._actualizar_totales()
        
        return self.obtener_resumen()
    def restar_cantidad(self, producto_id: int) -> Dict:
        """Actualiza la cantidad de un producto"""
        if producto_id in self.items:
            item = self.items[producto_id]
            if item.cantidad <= 1:
                return self.eliminar(producto_id)
            
            item.cantidad -= 1
            item.subtotal = item.precio * item.cantidad
            self._actualizar_totales()
        
        return self.obtener_resumen()
    
    def vaciar(self) -> Dict:
        """Vacía completamente el carrito"""
        self.items.clear()
        self.total = Decimal('0.00')
        self.total_items = 0
        return self.obtener_resumen()
    
    def _actualizar_totales(self):
        """Actualiza los totales del carrito"""
        self.total = Decimal('0.00')
        self.total_items = 0
        
        for item in self.items.values():
            self.total += item.subtotal
            self.total_items += item.cantidad
    
    def obtener_resumen(self) -> Dict:
        """Devuelve un resumen del carrito"""
        return {
            'items': list(self.items.values()),
            'total': float(self.total),
            'total_items': self.total_items,
            'cantidad_productos': len(self.items)
        }
    
    def obtener_item(self, producto_id: int) -> Optional[ItemCarrito]:
        """Obtiene un item específico del carrito"""
        return self.items.get(producto_id)
    
    def existe_producto(self, producto_id: int) -> bool:
        """Verifica si un producto está en el carrito"""
        return producto_id in self.items