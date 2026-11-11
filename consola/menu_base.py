from abc import ABC, abstractmethod
from entidades.usuario import Usuario

class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú correspondiente.
        Retorna True para cerrar sesión y volver al login, o False para salir del programa.
        """
        pass

def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("[Error] Debe ingresar un número entero válido.")

def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("[Error] Debe ingresar un número válido.")

def leer_texto(mensaje: str) -> str:
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("[Error] El texto no puede estar vacío.")