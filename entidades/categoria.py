from __future__ import annotations
from typing import TYPE_CHECKING
from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.producto import Producto


class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.__productos: list[Producto] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre de la categoría no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion = valor.strip()

    # --- Agregación con Producto ---
    @property
    def productos(self) -> tuple[Producto, ...]:
        return tuple(self.__productos)

    def productos_activos(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def _agregar_producto(self, producto: Producto) -> None:
        if producto not in self.__productos:
            self.__productos.append(producto)

    def _quitar_producto(self, producto: Producto) -> None:
        if producto in self.__productos:
            self.__productos.remove(producto)

    def __str__(self) -> str:
        return f"[{self.id}] Categoría: {self.nombre} - {self.descripcion}"
