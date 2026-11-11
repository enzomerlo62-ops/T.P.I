from abc import ABC , abstractmethod
from datetime import datetime
from excepciones.food_store_error import DatoInvalidoError

class Base(ABC):
    __contador_id: int = 0

    def __init__(self) -> None:
        Base.__contador_id += 1
        self.__id: int = Base.__contador_id
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()
      
          
    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("El valor de eliminado debe ser True o False.")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, Base):
            return self.__id == otro.__id
        return False
    
    def __hash__(self) -> int:
        return hash(self.__id)
    
    @abstractmethod
    def __str__(self) -> str:
        """Cada entidad debe definir cómo se muestra en los listados."""