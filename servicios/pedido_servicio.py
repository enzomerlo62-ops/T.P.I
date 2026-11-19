from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import EntidadNoEncontradaError, StockInsuficienteError, OperacionNoPermitidaError,DatoInvalidoError
from excepciones.food_store_error import EntidadNoEncontradaError, DatoInvalidoError


class PedidoServicio:
    def __init__(self) -> None:
        self._pedidos: list[Pedido] = []

    def listar(self) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado and p.usuario.id == usuario.id]

    def crear_pedido(self, usuario: Usuario, forma_pago: FormaPago, items: list[tuple[int, Producto]]) -> Pedido:
        if not items:
            raise DatoInvalidoError("El pedido debe tener al menos un producto")
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario eliminado.")
            
        nuevo_pedido = Pedido(usuario=usuario, forma_pago=forma_pago)
        
        # 1) Validar y agregar todos los detalles (agregar_detalle controla el stock
        #    contra la cantidad acumulada, por si el mismo producto aparece más de una vez)
        for cantidad, producto in items:
            if cantidad <= 0:
                raise OperacionNoPermitidaError("La cantidad del producto debe ser mayor a 0.")
            if cantidad > producto.stock:
                raise StockInsuficienteError(f"Stock insuficiente para el producto '{producto.nombre}'. Stock actual: {producto.stock}")
            nuevo_pedido.agregar_detalle(cantidad, producto)

        # 2) Recién cuando todo es válido, descontar el stock (si algo falló antes, no se tocó nada)
        for detalle in nuevo_pedido.detalles:
            detalle.producto.stock -= detalle.cantidad

        # Calcular total usando la interfaz Calculable
    def crear_pedido(self, usuario: Usuario, forma_pago: FormaPago,
                     items: list[tuple[int, Producto]]) -> Pedido:
        # Composición 1..m: un pedido tiene al menos un detalle
        if not items:
            raise DatoInvalidoError("El pedido debe tener al menos un producto.")

        nuevo_pedido = Pedido(usuario=usuario, forma_pago=forma_pago)

        # 1) Agregar todos los detalles: agregar_detalle valida cantidad, producto y stock
        for cantidad, producto in items:
            nuevo_pedido.agregar_detalle(cantidad, producto)

        # 2) Recién cuando todo es válido, descontar el stock (si algo falló, no se tocó nada)
        for detalle in nuevo_pedido.detalles:
            detalle.producto.stock -= detalle.cantidad

        # Total establecido con la interfaz Calculable
        nuevo_pedido.calcular_total()
        self._pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for p in self._pedidos:
            if p.id == id_pedido and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró el pedido con ID {id_pedido}.")

    def buscar_de_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        """Para el cliente: un pedido ajeno se informa como inexistente (HU-PED-05)."""
        pedido = self.buscar_por_id(id_pedido)
        if pedido.usuario.id != usuario.id:
            raise EntidadNoEncontradaError(f"No se encontró el pedido con ID {id_pedido}.")
        return pedido

    def actualizar_estado(self, id_pedido: int, nuevo_estado: Estado | None = None,
                          nueva_forma_pago: FormaPago | None = None) -> Pedido:
        """Cambia el estado y/o la forma de pago (None = conservar el valor actual)."""
        pedido = self.buscar_por_id(id_pedido)

        if nuevo_estado is not None:
            # El setter de Pedido valida la transición con TRANSICIONES:
            # si no es válida lanza OperacionNoPermitidaError y no cambia nada
            pedido.estado = nuevo_estado
            # Solo si el cambio fue válido se devuelve el stock
            if nuevo_estado == Estado.CANCELADO:
                for detalle in pedido.detalles:
                    detalle.producto.stock += detalle.cantidad

        if nueva_forma_pago is not None:
            pedido.forma_pago = nueva_forma_pago

        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            # Devolver stock si se elimina un pedido activo
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True
