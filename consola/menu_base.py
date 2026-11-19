from abc import ABC, abstractmethod
from enum import Enum
from entidades.usuario import Usuario


class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú correspondiente.
        Retorna True para cerrar sesión y volver al login, o False para salir del programa.
        """


# ---------------------------------------------------------------------
# Lectura validada: ningún dato mal ingresado cierra el programa
# ---------------------------------------------------------------------

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


def leer_texto_opcional(mensaje: str) -> str | None:
    """Para editar: Enter vacío devuelve None (= conservar el valor anterior)."""
    texto = input(mensaje).strip()
    return texto if texto else None


def leer_si_no(mensaje: str) -> bool:
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("[Error] Responda S o N.")


def leer_opcion_enum(mensaje: str, tipo: type[Enum]) -> Enum:
    """Muestra las opciones de un Enum numeradas y devuelve la elegida por número."""
    opciones = list(tipo)
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion.value}")
    while True:
        n = leer_entero(mensaje)
        if 1 <= n <= len(opciones):
            return opciones[n - 1]
        print(f"[Error] Elija un número entre 1 y {len(opciones)}.")
