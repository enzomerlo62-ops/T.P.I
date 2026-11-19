from consola.menu_base import (
    Menu, leer_entero, leer_flotante, leer_texto,
    leer_texto_opcional, leer_si_no, leer_opcion_enum,
)
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from entidades.base import Base
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import FoodStoreError


def mostrar_listado(elementos: list[Base], mensaje_vacio: str) -> bool:
    """Imprime un listado; si está vacío informa y devuelve False."""
    if not elementos:
        print(f"\n{mensaje_vacio}")
        return False
    for e in elementos:
        print(e)
    return True


class MenuAdministrador(Menu):
    def __init__(self, usuario: Usuario, cat_serv: CategoriaServicio, prod_serv: ProductoServicio,
                 usu_serv: UsuarioServicio, ped_serv: PedidoServicio) -> None:
        super().__init__(usuario)
        self._cat_serv = cat_serv
        self._prod_serv = prod_serv
        self._usu_serv = usu_serv
        self._ped_serv = ped_serv

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")

            opcion = leer_entero("Seleccione: ")

            if opcion == 1:
                self._ges_categorias()
            elif opcion == 2:
                self._ges_productos()
            elif opcion == 3:
                self._ges_usuarios()
            elif opcion == 4:
                self._ges_pedidos()
            elif opcion == 9:
                print("\nCerrando sesión...")
                return True
            elif opcion == 0:
                print("\nSaliendo del programa. ¡Hasta luego!")
                return False
            else:
                print("\n[Error] Opción fuera de rango.")

    # -----------------------------------------------------------------
    # CATEGORÍAS
    # -----------------------------------------------------------------
    def _ges_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    mostrar_listado(self._cat_serv.listar(), "No hay categorías cargadas.")
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    desc = leer_texto("Descripción: ")
                    c = self._cat_serv.crear(nom, desc)
                    print(f"\n[Éxito] Categoría creada con ID {c.id}.")
                elif op == 3:
                    if not mostrar_listado(self._cat_serv.listar(), "No hay categorías cargadas."):
                        continue
                    id_c = leer_entero("ID de categoría a editar: ")
                    self._cat_serv.buscar_por_id(id_c)          # si no existe, se informa antes de pedir datos
                    nom = leer_texto_opcional("Nuevo nombre (Enter para conservar): ")
                    desc = leer_texto_opcional("Nueva descripción (Enter para conservar): ")
                    self._cat_serv.editar(id_c, nom, desc)
                    print("\n[Éxito] Categoría actualizada.")
                elif op == 4:
                    if not mostrar_listado(self._cat_serv.listar(), "No hay categorías cargadas."):
                        continue
                    id_c = leer_entero("ID de categoría a eliminar: ")
                    self._cat_serv.buscar_por_id(id_c)
                    if leer_si_no("¿Confirma la eliminación? (S/N): "):
                        self._cat_serv.eliminar(id_c)
                        print("\n[Éxito] Categoría eliminada.")
                    else:
                        print("\n[Aviso] Operación cancelada.")
                elif op == 0:
                    return
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error] {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado] {e}")

    # -----------------------------------------------------------------
    # PRODUCTOS
    # -----------------------------------------------------------------
    def _ges_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    mostrar_listado(self._prod_serv.listar(), "No hay productos cargados.")
                elif op == 2:
                    if not mostrar_listado(self._cat_serv.listar(),
                                           "Primero debe crear una categoría."):
                        continue
                    id_cat = leer_entero("ID de categoría: ")
                    cat = self._cat_serv.buscar_por_id(id_cat)
                    nom = leer_texto("Nombre: ")
                    precio = leer_flotante("Precio: ")
                    desc = leer_texto("Descripción: ")
                    stock = leer_entero("Stock: ")
                    img = leer_texto("Imagen (url/nombre): ")
                    disp = leer_si_no("¿Disponible? (S/N): ")
                    p = self._prod_serv.crear(nom, precio, desc, stock, img, disp, cat)
                    print(f"\n[Éxito] Producto creado con ID {p.id}.")
                elif op == 3:
                    if not mostrar_listado(self._prod_serv.listar(), "No hay productos cargados."):
                        continue
                    id_p = leer_entero("ID de producto a editar: ")
                    self._prod_serv.buscar_por_id(id_p)
                    nom = leer_texto_opcional("Nuevo nombre (Enter para conservar): ")
                    p_str = leer_texto_opcional("Nuevo precio (Enter para conservar): ")
                    stock_str = leer_texto_opcional("Nuevo stock (Enter para conservar): ")
                    try:
                        precio = float(p_str) if p_str else None
                        stock = int(stock_str) if stock_str else None
                    except ValueError:
                        print("\n[Error] El precio debe ser un número y el stock un número entero.")
                        continue
                    self._prod_serv.editar(id_p, nom, precio, stock=stock)
                    print("\n[Éxito] Producto actualizado.")
                elif op == 4:
                    if not mostrar_listado(self._prod_serv.listar(), "No hay productos cargados."):
                        continue
                    id_p = leer_entero("ID de producto a eliminar: ")
                    self._prod_serv.buscar_por_id(id_p)
                    if leer_si_no("¿Confirma la eliminación? (S/N): "):
                        self._prod_serv.eliminar(id_p)
                        print("\n[Éxito] Producto eliminado.")
                    else:
                        print("\n[Aviso] Operación cancelada.")
                elif op == 0:
                    return
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error] {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado] {e}")

    # -----------------------------------------------------------------
    # USUARIOS
    # -----------------------------------------------------------------
    def _ges_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    mostrar_listado(self._usu_serv.listar(), "No hay usuarios cargados.")
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    ape = leer_texto("Apellido: ")
                    mail = leer_texto("Mail: ")
                    cel = leer_texto("Celular: ")
                    contra = leer_texto("Contraseña (mínimo 4 caracteres): ")
                    print("Rol:")
                    rol = leer_opcion_enum("Seleccione rol por número: ", Rol)
                    u = self._usu_serv.crear(nom, ape, mail, cel, contra, rol)
                    print(f"\n[Éxito] Usuario creado con ID {u.id}.")
                elif op == 3:
                    mostrar_listado(self._usu_serv.listar(), "No hay usuarios cargados.")
                    id_u = leer_entero("ID de usuario a editar: ")
                    usu = self._usu_serv.buscar_por_id(id_u)
                    nom = leer_texto_opcional(f"Nombre [{usu.nombre}] (Enter para conservar): ")
                    ape = leer_texto_opcional(f"Apellido [{usu.apellido}] (Enter para conservar): ")
                    mail = leer_texto_opcional(f"Mail [{usu.mail}] (Enter para conservar): ")
                    cel = leer_texto_opcional(f"Celular [{usu.celular}] (Enter para conservar): ")
                    rol = None
                    if leer_si_no(f"¿Cambiar el rol? Actual: {usu.rol.value} (S/N): "):
                        rol = leer_opcion_enum("Seleccione rol por número: ", Rol)
                    self._usu_serv.editar(id_u, nom, ape, mail, cel, rol)
                    print("\n[Éxito] Usuario actualizado.")
                elif op == 4:
                    mostrar_listado(self._usu_serv.listar(), "No hay usuarios cargados.")
                    id_u = leer_entero("ID de usuario a eliminar: ")
                    self._usu_serv.buscar_por_id(id_u)
                    if leer_si_no("¿Confirma la eliminación? (S/N): "):
                        self._usu_serv.eliminar(id_u, self._usuario.id)
                        print("\n[Éxito] Usuario eliminado.")
                    else:
                        print("\n[Aviso] Operación cancelada.")
                elif op == 0:
                    return
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error] {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado] {e}")

    # -----------------------------------------------------------------
    # PEDIDOS
    # -----------------------------------------------------------------
    def _ges_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar")
            print("2. Crear pedido")
            print("3. Cambiar estado / forma de pago")
            print("4. Eliminar pedido")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    mostrar_listado(self._ped_serv.listar(), "No hay pedidos cargados.")
                elif op == 2:
                    self._crear_pedido()
                elif op == 3:
                    if not mostrar_listado(self._ped_serv.listar(), "No hay pedidos cargados."):
                        continue
                    id_ped = leer_entero("ID del pedido a actualizar: ")
                    ped = self._ped_serv.buscar_por_id(id_ped)
                    estado = None
                    forma_pago = None
                    if leer_si_no(f"¿Cambiar el estado? Actual: {ped.estado.value} (S/N): "):
                        estado = leer_opcion_enum("Seleccione nuevo estado: ", Estado)
                    if leer_si_no(f"¿Cambiar la forma de pago? Actual: {ped.forma_pago.value} (S/N): "):
                        forma_pago = leer_opcion_enum("Seleccione forma de pago: ", FormaPago)
                    if estado is None and forma_pago is None:
                        print("\n[Aviso] No se realizaron cambios.")
                        continue
                    self._ped_serv.actualizar_estado(id_ped, estado, forma_pago)
                    print("\n[Éxito] Pedido actualizado.")
                elif op == 4:
                    if not mostrar_listado(self._ped_serv.listar(), "No hay pedidos cargados."):
                        continue
                    id_ped = leer_entero("ID del pedido a eliminar: ")
                    self._ped_serv.buscar_por_id(id_ped)
                    if leer_si_no("¿Confirma la eliminación? (S/N): "):
                        self._ped_serv.eliminar(id_ped)
                        print("\n[Éxito] Pedido eliminado.")
                    else:
                        print("\n[Aviso] Operación cancelada.")
                elif op == 0:
                    return
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error] {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado] {e}")

    def _crear_pedido(self) -> None:
        mostrar_listado(self._usu_serv.listar(), "No hay usuarios cargados.")
        id_u = leer_entero("ID del usuario cliente: ")
        usu = self._usu_serv.buscar_por_id(id_u)
        print("Forma de pago:")
        fp = leer_opcion_enum("Seleccione forma de pago por número: ", FormaPago)

        items: list[tuple[int, Producto]] = []
        print("\nProductos disponibles:")
        mostrar_listado(self._prod_serv.listar(solo_disponibles=True), "No hay productos disponibles.")
        while True:
            id_prod = leer_entero("ID del producto a agregar (0 para terminar): ")
            if id_prod == 0:
                break
            try:
                prod = self._prod_serv.buscar_por_id(id_prod)
            except FoodStoreError as e:
                print(f"[Error] {e}")
                continue
            cant = leer_entero("Cantidad: ")
            items.append((cant, prod))

        if not items:
            print("\n[Aviso] No se agregaron productos: el pedido no se creó.")
            return
        # Si algún detalle falla (ej.: falta de stock), el servicio lanza la excepción,
        # el pedido no se guarda y no se modifica ningún stock.
        ped = self._ped_serv.crear_pedido(usu, fp, items)
        print(f"\n[Éxito] Pedido #{ped.id} creado. Total: ${ped.total:.2f}")
