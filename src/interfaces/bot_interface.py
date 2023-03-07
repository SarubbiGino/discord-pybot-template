
from dataclasses import dataclass
from datetime import date
from abc import abstractmethod
from collections.abc import Callable, Awaitable
from interfaces.api_interface import ResCompararRegaloDeseos
from interfaces.app_interface import Participante


@dataclass
class Contexto:
    id_servidor: str = ''
    id_juego: str = ''
    id_participante: str = ''
    nombre_usuario: str = ''
    regalo: str = ''


class Bot:
    @abstractmethod
    def evento_iniciar_nuevo_server(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    def evento_iniciar_nuevo_server(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    def evento_preguntan_por_amigo(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    def evento_comunicar_amigo_invisible(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    def evento_comparar_sugerencia_con_deseos(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    def evento_agregar_regalo_a_lista(self, handler: Callable[[Contexto], Awaitable[None]]):
        raise NotImplementedError

    @abstractmethod
    async def dar_mensaje_bienvenida(self, id_servidor: str):
        raise NotImplementedError

    @abstractmethod
    async def mostrar_comandos_disponibles(self, id_servidor: str):
        raise NotImplementedError

    @abstractmethod
    async def solicitar_fecha_celebracion(self, id_servidor: str) -> date:
        raise NotImplementedError

    @abstractmethod
    async def enviar_nombre_amigo(self, id_participante: str, id_servidor: str, nombre_amigo: str):
        raise NotImplementedError

    @abstractmethod
    async def enviar_nombre_amigo_a_todos(self, id_juego: str, participantes: list[Participante]):
        raise NotImplementedError

    @abstractmethod
    async def enviar_resultados_por_sugerencia(self, id_juego: str, id_participante: str, resultados: ResCompararRegaloDeseos):
        raise NotImplementedError

    @abstractmethod
    async def mostrar_lista_deseos_amigo(self, id_juego: str, id_participante: str, lista_deseos_amigo: list[str]):
        raise NotImplementedError

    @abstractmethod
    async def comunicar_juego_no_fue_creado(self, id_servidor: str):
        raise NotImplementedError

    @abstractmethod
    async def comunicar_participante_no_fue_agregado(self, id_juego: str, nombre_usuario: str):
        raise NotImplementedError

    @abstractmethod
    async def comunicar_regalo_no_fue_agregado(self, id_juego: str, id_participante: str):
        raise NotImplementedError
