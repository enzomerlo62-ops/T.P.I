from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.excepciones_propias import EntidadNoEncontradaError, DuplicadoError, CredencialesInvalidasError, OperacionNoPermitidaError

class UsuarioServicio:
    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []
        # Cargar administrador inicial por defecto (exigido por el TPI)
        self.crear_admin_inicial()

    def crear_admin_inicial(self) -> None:
        admin = Usuario(
            nombre="Ana",
            apellido="Pérez",
            mail="admin@foodstore.com",
            celular="2610000000",
            contrasenia="admin123",
            rol=Rol.ADMIN
        )
        self._usuarios.append(admin)

    def listar(self) -> list[Usuario]:
        return [u for u in self._usuarios if not u.eliminado]

    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        for u in self._usuarios:
            if not u.eliminado and u.mail.strip().lower() == mail.strip().lower():
                raise DuplicadoError(f"El mail '{mail}' ya se encuentra registrado.")
        
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, mail=mail, celular=celular, contrasenia=contrasenia, rol=rol)
        self._usuarios.append(nuevo_usuario)
        return nuevo_usuario

    def buscar_por_id(self, id_usu: int) -> Usuario:
        for u in self._usuarios:
            if u.id == id_usu and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"No se encontró el usuario con ID {id_usu}.")

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        # Buscar usuario por mail
        usuario_encontrado = None
        for u in self._usuarios:
            if u.mail.strip().lower() == mail.strip().lower() and not u.eliminado:
                usuario_encontrado = u
                break
        
        # Si no existe, está eliminado, o la contraseña no coincide -> lanza CredencialesInvalidasError con mensaje genérico
        if not usuario_encontrado or not usuario_encontrado.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos.")
            
        return usuario_encontrado

    def eliminar(self, id_usu: int, id_usuario_actual: int) -> None:
        if id_usu == id_usuario_actual:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a sí mismo mientras tiene la sesión iniciada.")
        usu = self.buscar_por_id(id_usu)
        usu.eliminado = True