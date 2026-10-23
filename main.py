"""
Módulo Principal de la Aplicación (main.py)
Instancia FastAPI, expone los endpoints RESTful y gestiona excepciones.
"""

from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID

from models import Producto, ProductoCreate, ProductoUpdate
from database import db_productos, cargar_datos_semilla

# Instancia de FastAPI con metadata profesional
app = FastAPI(
    title="API Catálogo de Productos Efímero - SENA ADSO",
    description="API RESTful para la gestión de inventarios tecnológicos en memoria utilizando Pydantic y FastAPI",
    version="1.0.0"
)

# Cargar datos iniciales al arrancar la aplicación
@app.on_event("startup")
def startup_event():
    cargar_datos_semilla()

# ================================================
# ENDPOINTS Y LÓGICA DEL CRUD
# ================================================

@app.get(
    "/",
    tags=["Raíz"],
    summary="Mensaje de Bienvenida"
)
def welcome():
    return {
        "mensaje": "Bienvenido a la API del Catálogo de Productos Efímero (SENA ADSO)",
        "documentacion": "/docs"
    }


@app.get(
    "/productos",
    response_model=List[Producto],
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Obtener todo el inventario"
)
def get_productos():
    """Devuelve la lista completa de productos registrados en memoria."""
    return db_productos


@app.get(
    "/productos/{producto_id}",
    response_model=Producto,
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Buscar producto por ID"
)
def get_producto_por_id(producto_id: UUID):
    """
    Busca un producto específico mediante su identificador UUID.
    - Lanza **HTTP 404 Not Found** si el producto no existe en memoria.
    """
    for prod in db_productos:
        if prod.id == producto_id:
            return prod
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El producto con ID '{producto_id}' no fue encontrado en el catálogo."
    )


@app.post(
    "/productos",
    response_model=Producto,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"],
    summary="Agregar nuevo producto"
)
def create_producto(producto_in: ProductoCreate):
    """
    Crea un nuevo producto en el inventario:
    - Valida automáticamente que el `precio` sea mayor a 0 (gt=0).
    - Asigna un `id` UUIDv4 único de forma automática.
    - Lanza **HTTP 400 Bad Request** si el nombre ya se encuentra registrado.
    """
    # Validación personalizada: Evitar duplicados por nombre
    for prod in db_productos:
        if prod.nombre.lower() == producto_in.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un producto registrado con el nombre '{producto_in.nombre}'."
            )

    # Transformar el esquema de entrada al modelo completo con UUID
    nuevo_producto = Producto(**producto_in.model_dump())
    db_productos.append(nuevo_producto)
    return nuevo_producto


@app.put(
    "/productos/{producto_id}",
    response_model=Producto,
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Actualizar producto por ID"
)
def update_producto(producto_id: UUID, producto_update: ProductoUpdate):
    """
    Actualiza los datos de un producto existente por su ID UUID:
    - Reemplaza los campos proporcionados de forma segura.
    - Lanza **HTTP 404 Not Found** si el ID solicitado no existe.
    """
    for index, prod in enumerate(db_productos):
        if prod.id == producto_id:
            # Extraer solo los campos que fueron enviados en la petición
            datos_actualizados = producto_update.model_dump(exclude_unset=True)

            # Crear una copia actualizada del objeto manteniendo su ID original
            producto_modificado = prod.model_copy(update=datos_actualizados)
            db_productos[index] = producto_modificado
            return producto_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El producto con ID '{producto_id}' no existe."
    )


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Eliminar producto por ID"
)
def delete_producto(producto_id: UUID):
    """
    Elimina un registro del catálogo en memoria sin romper el índice de la lista:
    - Lanza **HTTP 404 Not Found** si el registro no existe.
    """
    for index, prod in enumerate(db_productos):
        if prod.id == producto_id:
            producto_eliminado = db_productos.pop(index)
            return {
                "mensaje": "Producto eliminado exitosamente",
                "producto_eliminado": producto_eliminado
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El producto con ID '{producto_id}' no existe."
    )