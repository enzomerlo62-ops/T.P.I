from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.usuario import Usuario
from entidades.producto import Producto
from entidades.detalle_pedido import DetallePedido
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import StockInsuficienteError, DatoInvalidoError


class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__forma_pago: FormaPago = forma_pago
        self.__usuario: Usuario = usuario
        self.__detalles: list[DetallePedido] = []
        self.__total: float = 0.0

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, nuevo_estado: Estado) -> None:
        self.__estado = nuevo_estado

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, nueva_forma: FormaPago) -> None:
        self.__forma_pago = nueva_forma

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0.")
        
        detalle_existente = self.buscar_detalle_por_producto(producto)
        cantidad_total = cantidad + (detalle_existente.cantidad if detalle_existente else 0)

        if cantidad_total > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
            )

        if detalle_existente:
            detalle_existente.cantidad = cantidad_total
        else:
            nuevo_detalle = DetallePedido(cantidad, producto)
            self.__detalles.append(nuevo_detalle)

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for d in self.__detalles:
            if d.producto == producto:
                return d
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle:
            self.__detalles.remove(detalle)

    def calcular_total(self) -> None:
        self.__total = round(sum(d.subtotal for d in self.__detalles), 2)

    def __str__(self) -> str:
        return (
            f"[{self.id}] Pedido de {self.usuario.nombre} {self.usuario.apellido} | "
            f"Fecha: {self.fecha} | Estado: {self.estado.value} | "
            f"Pago: {self.forma_pago.value} | Total: ${self.total:.2f}"
        )