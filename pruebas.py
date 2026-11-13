from entidades.pedido import Pedido
from entidades.usuario import Usuario
from enums.rol import Rol
from enums.forma_pago import FormaPago
from excepciones.food_store_error import DatoInvalidoError

u = Usuario("Ana", "Pérez", "ana@mail.com", "", "1234", Rol.USUARIO)

p = Pedido(u, FormaPago.EFECTIVO)
print("BIEN: pedido creado ->", p.forma_pago)

for valor in ("TARJETA", 1, None):
    try:
        Pedido(u, valor)
        print("MAL: aceptó", repr(valor))
    except DatoInvalidoError as e:
        print("BIEN: rechazó", repr(valor), "->", e)