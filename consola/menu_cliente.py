from consola.menu_base import Menu, leer_entero
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.pedido_servicio import PedidoServicio
from entidades.usuario import Usuario
from excepciones.food_store_error import FoodStoreError

class MenuCliente(Menu):
    def __init__(self, usuario: Usuario, categoria_servicio: CategoriaServicio, producto_servicio: ProductoServicio, pedido_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self._cat_serv = categoria_servicio
        self._prod_serv = producto_servicio
        self._ped_serv = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            
            opcion = leer_entero("Seleccione: ")
            
            try:
                if opcion == 1:
                    categorias = self._cat_serv.listar()
                    if not categorias:
                        print("\nNo hay categorías cargadas.")
                    else:
                        print("\n--- CATEGORÍAS ---")
                        for c in categorias:
                            print(c)
                elif opcion == 2:
                    productos = self._prod_serv.listar(solo_disponibles=True)
                    if not productos:
                        print("\nNo hay productos disponibles en este momento.")
                    else:
                        print("\n--- PRODUCTOS DISPONIBLES ---")
                        for p in productos:
                            print(p)
                elif opcion == 3:
                    pedidos = self._ped_serv.listar_por_usuario(self._usuario)
                    if not pedidos:
                        print("\nNo tienes pedidos registrados.")
                    else:
                        print("\n--- MIS PEDIDOS ---")
                        for p in pedidos:
                            print(p)
                        # Opción para ver detalles de un pedido propio
                        id_ped = leer_entero("Ingrese el ID del pedido para ver sus detalles (0 para volver): ")
                        if id_ped != 0:
                            pedido = self._ped_serv.buscar_por_id(id_ped)
                            if pedido.usuario.id != self._usuario.id:
                                print("\n[Error] El pedido no pertenece a tu usuario.")
                            else:
                                print(f"\nDetalles del Pedido #{pedido.id}:")
                                for det in pedido.detalles:
                                    print(f" - {det.producto.nombre} x {det.cantidad} un. (Subtotal: ${det.subtotal})")
                                print(f"Total a pagar: ${pedido.total}")
                elif opcion == 4:
                    print("\n--- MIS DATOS ---")
                    print(f"Nombre: {self._usuario.nombre} {self._usuario.apellido}")
                    print(f"Mail: {self._usuario.mail}")
                    print(f"Celular: {self._usuario.celular}")
                    print(f"Rol: {self._usuario.rol.name}")
                elif opcion == 9:
                    print("\nCerrando sesión...")
                    return True
                elif opcion == 0:
                    print("\nSaliendo del programa. ¡Hasta luego!")
                    return False
                else:
                    print("\n[Error] Opción fuera de rango. Intente nuevamente.")
            except FoodStoreError as e:
                print(f"\n[Error de Negocio]: {e}")