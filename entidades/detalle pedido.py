from entidades.base import Base
from entidades.producto import Producto


class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__cantidad = cantidad
        self.__producto = producto
        self.__subtotal = round(cantidad * producto.precio, 2)

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = valor
        self.__subtotal = round(self.__cantidad * self.__producto.precio, 2)

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @property
    def producto(self) -> Producto:
        return self.__producto

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} - Subtotal: ${self.subtotal:.2f}"