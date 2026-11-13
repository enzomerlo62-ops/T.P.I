from entidades.categoria import Categoria
from excepciones.food_store_error import EntidadNoEncontradaError, DuplicadoError, OperacionNoPermitidaError

class CategoriaServicio:
    def __init__(self) -> None:
        self._categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        return [c for c in self._categorias if not c.eliminado]

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        # Validar nombre único sin distinguir mayúsculas
        for cat in self._categorias:
            if not cat.eliminado and cat.nombre.strip().lower() == nombre.strip().lower():
                raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'.")
        
        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        self._categorias.append(nueva_categoria)
        return nueva_categoria

    def buscar_por_id(self, id_cat: int) -> Categoria:
        for cat in self._categorias:
            if cat.id == id_cat and not cat.eliminado:
                return cat
        raise EntidadNoEncontradaError(f"No se encontró la categoría con ID {id_cat}.")

    def editar(self, id_cat: int, nombre: str | None = None, descripcion: str | None = None) -> Categoria:
        cat = self.buscar_por_id(id_cat)
        
        if nombre is not None and nombre.strip() != "":
            # Validar unicidad si cambia el nombre
            for c in self._categorias:
                if not c.eliminado and c.id != id_cat and c.nombre.strip().lower() == nombre.strip().lower():
                    raise DuplicadoError(f"Ya existe otra categoría con el nombre '{nombre}'.")
            cat.nombre = nombre
            
        if descripcion is not None and descripcion.strip() != "":
            cat.descripcion = descripcion
            
        return cat

    def eliminar(self, id_cat: int, productos_asociados_activos: int = 0) -> None:
        cat = self.buscar_por_id(id_cat)
        if productos_asociados_activos > 0:
            raise OperacionNoPermitidaError("No se puede eliminar una categoría con productos activos.")
        cat.eliminado = True