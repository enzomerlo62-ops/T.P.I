from consola.menu_base import Menu, leer_entero, leer_flotante, leer_texto
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from entidades.usuario import Usuario
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import FoodStoreError

class MenuAdministrador(Menu):
    def __init__(self, usuario: Usuario, cat_serv: CategoriaServicio, prod_serv: ProductoServicio, usu_serv: UsuarioServicio, ped_serv: PedidoServicio) -> None:
        super().__init__(usuario)
        self._cat_serv = cat_serv
        self._prod_serv = prod_serv
        self._usu_serv = usu_serv
        self._ped_serv = ped_serv

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            
            opcion = leer_entero("Seleccione: ")
            
            if opcion == 1:
                if not self._ges_categorias():
                    return False
            elif opcion == 2:
                if not self._ges_productos():
                    return False
            elif opcion == 3:
                if not self._ges_usuarios():
                    return False
            elif opcion == 4:
                if not self._ges_pedidos():
                    return False
            elif opcion == 9:
                print("\nCerrando sesión...")
                return True
            elif opcion == 0:
                print("\nSaliendo del programa. ¡Hasta luego!")
                return False
            else:
                print("\n[Error] Opción fuera de rango.")

    def _ges_categorias(self) -> bool:
        while True:
            print("\n--- GESTIÓN DE CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    cats = self._cat_serv.listar()
                    for c in cats: print(c)
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    desc = leer_texto("Descripción: ")
                    c = self._cat_serv.crear(nom, desc)
                    print(f"\n[Éxito] Categoría creada con ID {c.id}.")
                elif op == 3:
                    id_c = leer_entero("ID de categoría a editar: ")
                    nom = input("Nuevo nombre (Enter para conservar): ")
                    desc = input("Nueva descripción (Enter para conservar): ")
                    self._cat_serv.editar(id_c, nom if nom else None, desc if desc else None)
                    print("\n[Éxito] Categoría actualizada.")
                elif op == 4:
                    id_c = leer_entero("ID de categoría a eliminar: ")
                    # Contar productos asociados activos
                    prods = [p for p in self._prod_serv.listar() if p.categoria.id == id_c]
                    self._cat_serv.eliminar(id_c, len(prods))
                    print("\n[Éxito] Categoría eliminada lógicamente.")
                elif op == 0:
                    break
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error]: {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado]: {e}")
        return True

    def _ges_productos(self) -> bool:
        while True:
            print("\n--- GESTIÓN DE PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    for p in self._prod_serv.listar(): print(p)
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    precio = leer_flotante("Precio: ")
                    desc = leer_texto("Descripción: ")
                    stock = leer_entero("Stock: ")
                    img = leer_texto("Imagen (url/nombre): ")
                    disp_str = leer_texto("¿Disponible? (S/N): ").upper()
                    disp = True if disp_str == 'S' else False
                    id_cat = leer_entero("ID de Categoría: ")
                    cat = self._cat_serv.buscar_por_id(id_cat)
                    p = self._prod_serv.crear(nom, precio, desc, stock, img, disp, cat)
                    print(f"\n[Éxito] Producto creado con ID {p.id}.")
                elif op == 3:
                    id_p = leer_entero("ID de producto a editar: ")
                    nom = input("Nuevo nombre (Enter para conservar): ")
                    p_str = input("Nuevo precio (Enter para conservar): ").strip()
                    stock_str = input("Nuevo stock (Enter para conservar): ").strip()
                    try:
                        precio = float(p_str) if p_str else None
                        stock = int(stock_str) if stock_str else None
                    except ValueError:
                        print("\n[Error] El precio debe ser un número y el stock un número entero.")
                        continue
                    self._prod_serv.editar(id_p, nom if nom else None, precio, stock=stock)
                    print("\n[Éxito] Producto actualizado.")
                elif op == 4:
                    id_p = leer_entero("ID de producto a eliminar: ")
                    self._prod_serv.eliminar(id_p)
                    print("\n[Éxito] Producto eliminado lógicamente.")
                elif op == 0:
                    break
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error]: {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado]: {e}")
        return True

    def _ges_usuarios(self) -> bool:
        while True:
            print("\n--- GESTIÓN DE USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    for u in self._usu_serv.listar(): print(u)
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    ape = leer_texto("Apellido: ")
                    mail = leer_texto("Mail: ")
                    cel = leer_texto("Celular: ")
                    contra = leer_texto("Contraseña: ")
                    print("Roles: 1. ADMIN | 2. USUARIO")
                    r_op = leer_entero("Seleccione rol por número: ")
                    rol = Rol.ADMIN if r_op == 1 else Rol.USUARIO
                    u = self._usu_serv.crear(nom, ape, mail, cel, contra, rol)
                    print(f"\n[Éxito] Usuario creado con ID {u.id}.")
                elif op == 3:
                    id_u = leer_entero("ID de usuario a eliminar: ")
                    self._usu_serv.eliminar(id_u, self._usuario.id)
                    print("\n[Éxito] Usuario eliminado lógicamente.")
                elif op == 0:
                    break
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error]: {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado]: {e}")
        return True

    def _ges_pedidos(self) -> bool:
        while True:
            print("\n--- GESTIÓN DE PEDIDOS ---")
            print("1. Listar")
            print("2. Crear Pedido")
            print("3. Cambiar Estado / Forma de Pago")
            print("4. Eliminar Pedido")
            print("0. Volver")
            op = leer_entero("Seleccione: ")
            try:
                if op == 1:
                    for p in self._ped_serv.listar(): print(p)
                elif op == 2:
                    id_u = leer_entero("ID del Usuario cliente: ")
                    usu = self._usu_serv.buscar_por_id(id_u)
                    print("Formas de Pago: 1. TARJETA | 2. TRANSFERENCIA | 3. EFECTIVO")
                    fp_op = leer_entero("Seleccione forma de pago por número: ")
                    fp = FormaPago.TARJETA if fp_op == 1 else (FormaPago.TRANSFERENCIA if fp_op == 2 else FormaPago.EFECTIVO)
                    
                    items = []
                    while True:
                        id_prod = leer_entero("ID del Producto a agregar (0 para terminar): ")
                        if id_prod == 0: break
                        cant = leer_entero("Cantidad: ")
                        prod = self._prod_serv.buscar_por_id(id_prod)
                        items.append((cant, prod))
                    
                    if items:
                        ped = self._ped_serv.crear_pedido(usu, fp, items)
                        print(f"\n[Éxito] Pedido #{ped.id} creado con total: ${ped.total}")
                    else:
                        print("\n[Aviso] No se agregaron productos, pedido cancelado.")
                elif op == 3:
                    id_ped = leer_entero("ID del Pedido a actualizar: ")
                    print("Estados: 1. PENDIENTE | 2. CONFIRMADO | 3. TERMINADO | 4. CANCELADO")
                    e_op = leer_entero("Seleccione nuevo estado: ")
                    if e_op not in (1, 2, 3, 4):
                        print("\n[Error] Opción de estado fuera de rango.")
                        continue
                    estado =[Estado.PENDIENTE, Estado.CONFIRMADO, Estado.TERMINADO, Estado.CANCELADO][e_op - 1]
                    self._ped_serv.actualizar_estado(id_ped, estado)
                    print("\n[Éxito] Estado de pedido actualizado.")
                elif op == 4:
                    id_ped = leer_entero("ID del pedido a eliminar: ")
                    self._ped_serv.eliminar(id_ped)
                    print("\n[Éxito] Pedido eliminado lógicamente.")
                elif op == 0:
                    break
                else:
                    print("\n[Error] Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"\n[Error]: {e}")
            except Exception as e:
                # Pauta: un error nunca cierra el programa; se informa y se vuelve al menú
                print(f"\n[Error inesperado]: {e}")
        return True