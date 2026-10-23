"""
Módulo de Base de Datos en Memoria (database.py)
Almacena temporalmente los objetos durante la ejecución de Uvicorn.
"""

from typing import List
from models import Producto
from uuid import uuid4

# Lista global que actúa como nuestra tabla de productos
db_productos: List[Producto] = []

def cargar_datos_semilla():
    """Carga registros iniciales de prueba (Seed Data) al iniciar la API"""
    if not db_productos:
        db_productos.extend([
            Producto(
                id=uuid4(),
                nombre="Laptop Asus ROG Strix",
                precio=5200000.0,
                disponible=True
            ),
            Producto(
                id=uuid4(),
                nombre="Mouse Inalámbrico Logitech MX Master 3S",
                precio=480000.0,
                disponible=True
            ),
            Producto(
                id=uuid4(),
                nombre="Teclado Mecánico Keychron K2 V2",
                precio=390000.0,
                disponible=False
            )
        ])