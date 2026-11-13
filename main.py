from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from enums.rol import Rol
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from excepciones.food_store_error import CredencialesInvalidasError

def crear_menu(usuario, cat_serv, prod_serv, usu_serv, ped_serv):
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, cat_serv, prod_serv, usu_serv, ped_serv)
    return MenuCliente(usuario, cat_serv, prod_serv, ped_serv)

def main() -> None:
    # Inicializar servicios en memoria
    cat_serv = CategoriaServicio()
    prod_serv = ProductoServicio()
    usu_serv = UsuarioServicio()
    ped_serv = PedidoServicio()

    print("=== INICIALIZANDO FOOD STORE ===")
    
    # Bucle general del programa (permite volver al login al cerrar sesión)
    while True:
        intentos = 3
        usuario_actual = None

        # Ciclo de inicio de sesión (máximo 3 intentos)
        while intentos > 0:
            print(f"\n=== FOOD STORE INICIO DE SESIÓN (Intentos restantes: {intentos}) ===")
            mail = input("Mail: ").strip()
            contrasenia = input("Contraseña: ").strip()

            try:
                usuario_actual = usu_serv.autenticar(mail, contrasenia)
                print(f"\nBienvenido/a, {usuario_actual.nombre} {usuario_actual.apellido} [{usuario_actual.rol.name}]")
                break
            except CredencialesInvalidasError:
                intentos -= 1
                print("\n[Error] Mail o contraseña incorrectos.")

        if intentos == 0:
            print("\n[Aviso] Se agotaron los 3 intentos permitidos. El programa ha finalizado.")
            break

        # Crear el menú según el rol (Polimorfismo puro)
        menu = crear_menu(usuario_actual, cat_serv, prod_serv, usu_serv, ped_serv)
        
        # Mostrar menú y evaluar si retorna True (cerrar sesión) o False (salir)
        continuar = menu.mostrar()
        if not continuar:
            break

if __name__ == "__main__":
    main()