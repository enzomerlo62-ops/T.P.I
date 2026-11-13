class FoodStoreError(Exception):
    """Excepción base para el dominio Food Store."""
    


class EntidadNoEncontradaError(FoodStoreError):
    """ Id inexistente o entidad no encontrada """


class DatoInvalidoError(FoodStoreError):
    """ Texto vació, formato incorrecto o tipo de dato inválido """


class PrecioInvalidoError(DatoInvalidoError):
    """ Precio no númerico o negativo """


class StockInsuficienteError(FoodStoreError):
    """ Cantidad pedida mayor al stock disponible """


class DuplicadoError(FoodStoreError):
    """ Mail de usuario o nombre de categoría repetido"""


class OperacionNoPermitidaError(FoodStoreError):
    """ Regla de negocio violada: transición de estado inválida: categoría con productos activos, administrador que intenta eliminarse,etc """


class CredencialesInvalidasError(FoodStoreError):
    """ Mail o contraseña incorrectos, o usuario eliminado."""