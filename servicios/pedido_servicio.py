from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import EntidadNoEncontradaError, StockInsuficienteError, OperacionNoPermitidaError

class PedidoServicio:
    def __init__(self) -> None:
        self._pedidos: list[Pedido] = []

    def listar(self) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado and p.usuario.id == usuario.id]

    def crear_pedido(self, usuario: Usuario, forma_pago: FormaPago, items: list[tuple[int, Producto]]) -> Pedido:
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario eliminado.")
            
        nuevo_pedido = Pedido(usuario=usuario, forma_pago=forma_pago)
        
        # Validar y agregar detalles descontando stock temporalmente
        for cantidad, producto in items:
            if cantidad <= 0:
                raise OperacionNoPermitidaError("La cantidad del producto debe ser mayor a 0.")
            if cantidad > producto.stock:
                raise StockInsuficienteError(f"Stock insuficiente para el producto '{producto.nombre}'. Stock actual: {producto.stock}")
            
            # Descontar stock
            producto.stock -= cantidad
            # Agregar detalle al pedido
            nuevo_pedido.agregar_detalle(cantidad, producto)
            
        # Calcular total usando la interfaz Calculable
        nuevo_pedido.calcular_total()
        self._pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for p in self._pedidos:
            if p.id == id_pedido and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró el pedido con ID {id_pedido}.")

    def actualizar_estado(self, id_pedido: int, nuevo_estado: Estado, nueva_forma_pago: FormaPago | None = None) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        
        # Validar transiciones de estado
        # PENDIENTE -> CONFIRMADO -> TERMINADO
        # PENDIENTE o CONFIRMADO -> CANCELADO
        estado_actual = pedido.estado
        
        if estado_actual in [Estado.TERMINADO, Estado.CANCELADO]:
            raise OperacionNoPermitidaError("Un pedido Terminado o Cancelado no puede cambiar de estado.")
            
        if nuevo_estado == Estado.CANCELADO:
            # Devolver stock al cancelar
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
        elif estado_actual == Estado.PENDIENTE and nuevo_estado not in [Estado.CONFIRMADO, Estado.CANCELADO]:
            raise OperacionNoPermitidaError("Transición de estado inválida desde PENDIENTE.")
        elif estado_actual == Estado.CONFIRMADO and nuevo_estado not in [Estado.TERMINADO, Estado.CANCELADO]:
            raise OperacionNoPermitidaError("Transición de estado inválida desde CONFIRMADO.")

        pedido.estado = nuevo_estado
        if nueva_forma_pago:
            pedido.forma_pago = nueva_forma_pago
            
        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in [Estado.TERMINADO, Estado.CANCELADO]:
            # Devolver stock si se elimina un pedido activo
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True