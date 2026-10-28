from abc import ABC, abstractmethod


class Calculable(ABC):
    @abstractmethod
    def calcular_total(self) -> None:
        """Método abstracto para calcular y actualizar el total del objeto."""
        pass