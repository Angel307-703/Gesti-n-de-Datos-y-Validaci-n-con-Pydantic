"""
Módulo de Modelos de Datos (models.py)
Define la estructura, tipos de datos y validaciones con Pydantic.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class ProductoBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del producto tecnológico",
        example="Laptop Gaming RTX 4060"
    )
    precio: float = Field(
        ...,
        gt=0,
        description="Precio unitario en COP/USD. Debe ser estrictamente mayor a 0",
        example=4500000.00
    )
    disponible: bool = Field(
        default=True,
        description="Estado de disponibilidad en el inventario"
    )

class ProductoCreate(ProductoBase):
    """Modelo utilizado para recibir solicitudes POST de creación"""
    pass

class ProductoUpdate(BaseModel):
    """Modelo para solicitudes PUT (Campos opcionales para edición)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    disponible: Optional[bool] = None

class Producto(ProductoBase):
    """Modelo completo de respuesta que incluye el ID único autogenerado"""
    id: UUID = Field(default_factory=uuid4, description="Identificador Único Universal (UUIDv4)")

    class Config:
        from_attributes = True