from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_error import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("El detalle debe tener un producto valido")
        self.__validar_cantidad(cantidad)
        super().__init__()
        self.__producto : Producto = producto
        self.__precio_unitario : float = producto.precio                    # precio congelado
        self.__cantidad : int = cantidad
        self.__actualizar_subtotal()
        

#-------------- Validación y calculo interno un solo lugar -----------------------

    @stacticmethod
    def __validar_cantidad(cantidad:int)  -> None:
        if not isinstance(cantidad,int) or isinstance(cantidad,bool) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser un número entero mayor a 0.")
        
    def _actualizar_subtotal(self) -> None:
        self.__subtotal: float = round(self.__cantidad * self.__precio_unitario, 2)
    
#-------------- Solo lo usa Pedido, al agregar de nuevo el mismo producto ------------

    def _sumar_cantidad(self,cantidad:int) -> None:
        self.__validar_cantidad(cantidad)
        self.__cantidad += cantidad
        self._actualizar_subtotal()
        
#--------- Property de solo Lectura ---------------------------------

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def precio_unitario(self):
        return self.__precio_unitario

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @property
    def producto(self) -> Producto:
        return self.__producto

    def __str__(self) -> str:
        return (f"{self.producto.nombre} x {self.cantidad} "
               f" (${self.__precio_unitario:.2f} c/u) - Subtotal: ${self.subtotal:.2f}")