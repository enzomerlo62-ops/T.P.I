from entidades.producto import Producto
from entidades.categoria import Categoria
from excepciones.excepciones_propias import EntidadNoEncontradaError, PrecioInvalidoError

class ProductoServicio:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def listar(self, solo_disponibles: bool = False) -> list[Producto]:
        if solo_disponibles:
            return [p for p in self._productos if not p.eliminado and p.disponible and p.stock > 0]
        return [p for p in self._productos if not p.eliminado]

    def crear(self, nombre: str, precio: float, descripcion: str, stock: int, imagen: str, disponible: bool, categoria: Categoria) -> Producto:
        nuevo_prod = Producto(nombre=nombre, precio=precio, descripcion=descripcion, stock=stock, imagen=imagen, disponible=disponible, categoria=categoria)
        self._productos.append(nuevo_prod)
        return nuevo_prod

    def buscar_por_id(self, id_prod: int) -> Producto:
        for prod in self._productos:
            if prod.id == id_prod and not prod.eliminado:
                return prod
        raise EntidadNoEncontradaError(f"No se encontró el producto con ID {id_prod}.")

    def editar(self, id_prod: int, nombre: str | None = None, precio: float | None = None, descripcion: str | None = None, stock: int | None = None, disponible: bool | None = None) -> Producto:
        prod = self.buscar_por_id(id_prod)
        if nombre is not None and nombre.strip() != "":
            prod.nombre = nombre
        if precio is not None:
            prod.precio = precio
        if descripcion is not None and descripcion.strip() != "":
            prod.descripcion = descripcion
        if stock is not None:
            prod.stock = stock
        if disponible is not None:
            prod.disponible = disponible
        return prod

    def eliminar(self, id_prod: int) -> None:
        prod = self.buscar_por_id(id_prod)
        prod.eliminado = True