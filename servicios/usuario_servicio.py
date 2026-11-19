from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.food_store_error import EntidadNoEncontradaError, DuplicadoError, CredencialesInvalidasError, OperacionNoPermitidaError
from excepciones.food_store_error import (
    EntidadNoEncontradaError, DuplicadoError,
    CredencialesInvalidasError, OperacionNoPermitidaError,
)


class UsuarioServicio:
    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []
        # Cargar administrador inicial por defecto
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

    # --- Regla de negocio: mail único (la usan crear y editar) ---
    def __validar_mail_unico(self, mail: str, id_excluido: int | None = None) -> None:
        for u in self._usuarios:
            if (not u.eliminado and u.id != id_excluido
                    and u.mail.strip().lower() == mail.strip().lower()):
                raise DuplicadoError(f"El mail '{mail}' ya se encuentra registrado.")

    def crear(self, nombre: str, apellido: str, mail: str, celular: str,
              contrasenia: str, rol: Rol) -> Usuario:
        self.__validar_mail_unico(mail)
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, mail=mail,
                                celular=celular, contrasenia=contrasenia, rol=rol)
        self._usuarios.append(nuevo_usuario)
        return nuevo_usuario

    def buscar_por_id(self, id_usu: int) -> Usuario:
        for u in self._usuarios:
            if u.id == id_usu and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"No se encontró el usuario con ID {id_usu}.")

    def editar(self, id_usu: int, nombre: str | None = None, apellido: str | None = None,
               mail: str | None = None, celular: str | None = None,
               rol: Rol | None = None) -> Usuario:
        """Actualiza solo los campos recibidos (None = conservar el valor actual)."""
        usu = self.buscar_por_id(id_usu)
        # Validar el mail ANTES de modificar nada, para no dejar el usuario a medio editar
        if mail is not None:
            self.__validar_mail_unico(mail, id_excluido=id_usu)
        if nombre is not None:
            usu.nombre = nombre
        if apellido is not None:
            usu.apellido = apellido
        if mail is not None:
            usu.mail = mail
        if celular is not None:
            usu.celular = celular
        if rol is not None:
            usu.rol = rol
        return usu

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        usuario_encontrado = None
        for u in self._usuarios:
            if u.mail.strip().lower() == mail.strip().lower() and not u.eliminado:
                usuario_encontrado = u
                break

        # Mismo mensaje en los tres casos: mail inexistente, usuario eliminado o contraseña incorrecta
        if not usuario_encontrado or not usuario_encontrado.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos.")

        return usuario_encontrado

    def eliminar(self, id_usu: int, id_usuario_actual: int) -> None:
        if id_usu == id_usuario_actual:
            raise OperacionNoPermitidaError(
                "Un administrador no puede eliminarse a sí mismo mientras tiene la sesión iniciada."
            )
        usu = self.buscar_por_id(id_usu)
        usu.eliminado = True
