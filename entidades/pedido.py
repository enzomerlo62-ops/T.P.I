from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.usuario import Usuario
from entidades.producto import Producto
from entidades.detalle_pedido import DetallePedido
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import (StockInsuficienteError, DatoInvalidoError,
 OperacionNoPermitidaError,EntidadNoEncontradaError)




class Pedido(Base, Calculable):
    
    TRANSICIONES: dict[Estado, tuple[Estado,...]] = {
        Estado.PENDIENTE : (Estado.CONFIRMADO,Estado.CANCELADO),        #la regla queda escrita como datos, en un solo lugar y fácil de leer. 
                                                                        #Si mañana aparece un estado nuevo, por ejemplo EN_CAMINO,
                                                                        # se agrega una fila al diccionario y no hay que tocar la lógica del setter.
        Estado.CONFIRMADO : (Estado.TERMINADO,Estado.CANCELADO),
        Estado.TERMINADO: (),
        Estado.CANCELADO: (),
    }
    
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        if not isinstance(usuario,Usuario):
            raise DatoInvalidoError("El pedido debe tener un usuario valido.")
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido para un usuario eliminado")
        super().__init__()
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.forma_pago = forma_pago        # -> pasa por el setter
        self.__usuario: Usuario = usuario
        self.__detalles: list[DetallePedido] = []
        self.__total: int = 0.0

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, nuevo_estado: Estado) -> None:
        if not isinstance(nuevo_estado,Estado):                       
            raise DatoInvalidoError("El estado no pertenece a la clase Estado.")
        if nuevo_estado not in self.TRANSICIONES[self.__estado]:                        #“si no es válida, se informa y no cambia nada”
            raise OperacionNoPermitidaError(f"No se puede pasar de {self.__estado.value} a {nuevo_estado.value}.")
        self.__estado = nuevo_estado


    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, nueva_forma: FormaPago) -> None:
        if not isinstance(nueva_forma,FormaPago):                       # 1. valida
            raise DatoInvalidoError("La forma de pago no es valida")
        self.__forma_pago = nueva_forma                                 # 2. guarda en el atributo PRIVADO

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
        # validar los datos de entrada antes de usarlos
        if not isinstance(cantidad,int) or isinstance(cantidad,bool) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser un número entero mayor a 0.")
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("Debe indicar un producto valido")
        
        # Regla de negocio sobre el producto
        if producto.eliminado or not producto.disponible:
            raise OperacionNoPermitidaError(f"El producto {producto.nombre} no esta disponible para pedidos.")
        
        # Control de stock contra la cantidad ACUMULADA(no se descuenta acá)
        
        detalle_existente = self.buscar_detalle_por_producto(producto)
        cantidad_total = cantidad + (detalle_existente.cantidad if detalle_existente else 0)
        if cantidad_total > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para {producto.nombre}. "
                f"Disponible: {producto.stock}, solicitado: {cantidad_total}."
            )
        # Sumar al detalle existente o crear uno nuevo:
        if detalle_existente:
            detalle_existente._sumar_cantidad(cantidad)
        else:
            nuevo_detalle = DetallePedido(cantidad, producto)
            self.__detalles.append(nuevo_detalle)
            
        self.calcular_total()                                   # <- el total nunca queda desactualizado

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for d in self.__detalles:
            if d.producto == producto:
                return d
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError("Ese producto no esta en el pedido")
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = round((sum(d.subtotal for d in self.__detalles),0.0), 2)

    def __str__(self) -> str:
        return (
            f"[{self.id}] Pedido de {self.usuario.nombre} {self.usuario.apellido} | "
            f"Fecha: {self.fecha} | Estado: {self.estado.value} | "
            f"Pago: {self.forma_pago.value} | Total: ${self.total:.2f}"
        )