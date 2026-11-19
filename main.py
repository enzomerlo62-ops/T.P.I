from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from entidades.usuario import Usuario
from enums.rol import Rol
from enums.forma_pago import FormaPago
from consola.menu_base import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from excepciones.food_store_error import CredencialesInvalidasError


def crear_menu(usuario: Usuario, cat_serv: CategoriaServicio, prod_serv: ProductoServicio,
               usu_serv: UsuarioServicio, ped_serv: PedidoServicio) -> Menu:
    """Único lugar donde se pregunta el rol: después solo se llama a menu.mostrar()."""
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, cat_serv, prod_serv, usu_serv, ped_serv)
    return MenuCliente(usuario, cat_serv, prod_serv, ped_serv)


def cargar_datos_ejemplo(cat_serv: CategoriaServicio, prod_serv: ProductoServicio,
                         usu_serv: UsuarioServicio, ped_serv: PedidoServicio) -> None:
    """Carga datos de prueba a través de los servicios (así se aplican todas las validaciones)."""
    pizzas = cat_serv.crear("Pizzas", "Pizzas a la piedra")
    bebidas = cat_serv.crear("Bebidas", "Bebidas frías")
    cat_serv.crear("Postres", "Postres caseros")            # sin productos: se puede eliminar

    muzza = prod_serv.crear("Muzza", 8500, "Muzzarella y aceitunas", 10, "muzza.png", True, pizzas)
    prod_serv.crear("Napolitana", 9500, "Tomate y ajo", 2, "napo.png", True, pizzas)   # stock bajo
    coca = prod_serv.crear("Coca-Cola 1.5L", 3000, "Gaseosa", 20, "coca.png", True, bebidas)
    prod_serv.crear("Agua mineral", 1500, "Sin gas", 0, "agua.png", True, bebidas)     # sin stock

    usu_serv.crear("Juan", "Gómez", "juan@mail.com", "2615551234", "juan1234", Rol.USUARIO)
    maria = usu_serv.crear("María", "López", "maria@mail.com", "2615559876", "maria1234", Rol.USUARIO)

    ped_serv.crear_pedido(maria, FormaPago.EFECTIVO, [(1, muzza), (2, coca)])


def main() -> None:
    # Servicios en memoria: se crean acá y se pasan a los menús (no hay variables globales)
    cat_serv = CategoriaServicio()
    prod_serv = ProductoServicio()
    usu_serv = UsuarioServicio()            # carga el administrador inicial
    ped_serv = PedidoServicio()
    cargar_datos_ejemplo(cat_serv, prod_serv, usu_serv, ped_serv)

    print("=== INICIALIZANDO FOOD STORE ===")

    # Bucle general del programa (permite volver al login al cerrar sesión)
    while True:
        intentos = 3
        usuario_actual = None

        # Ciclo de inicio de sesión (máximo 3 intentos)
        while intentos > 0:
            print(f"\n=== FOOD STORE – INICIO DE SESIÓN (Intentos restantes: {intentos}) ===")
            mail = input("Mail: ").strip()
            contrasenia = input("Contraseña: ").strip()

            try:
                usuario_actual = usu_serv.autenticar(mail, contrasenia)
                print(f"\nBienvenido/a, {usuario_actual.nombre} {usuario_actual.apellido} "
                      f"[{usuario_actual.rol.name}]")
                break
            except CredencialesInvalidasError as e:
                intentos -= 1
                print(f"\n[Error] {e}")

        if usuario_actual is None:
            print("\n[Aviso] Se agotaron los 3 intentos permitidos. El programa ha finalizado.")
            break

        # Crear el menú según el rol (polimorfismo)
        menu = crear_menu(usuario_actual, cat_serv, prod_serv, usu_serv, ped_serv)

        # True = cerrar sesión (vuelve al login), False = salir del programa
        if not menu.mostrar():
            break


if __name__ == "__main__":
    main()