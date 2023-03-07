
from dataclasses import dataclass
from abc import abstractmethod
from interfaces.app_interface import Participante


@dataclass
class ResCrearJuego:
    fue_creado: bool = False


@dataclass
class ResAgregarParticipante:
    fue_agregado: bool = False


@dataclass
class ResCompararRegaloDeseos:
    fue_acertado: bool = False
    puntos_obtenidos: int = 0
    puntos_totales: int = 0


@dataclass
class ResAgregarRegalo:
    fue_agregado: bool = False


class Api:
    @ abstractmethod
    def run(self):
        raise NotImplementedError

    @ abstractmethod
    async def crear_nuevo_juego(self) -> ResCrearJuego:
        raise NotImplementedError

    @ abstractmethod
    async def recuperar_nombre_amigo(self, id_particpante: str) -> str:
        raise NotImplementedError

    @ abstractmethod
    async def agregar_particpante(self, id_juego: str, nombre_usuario) -> ResAgregarParticipante:
        raise NotImplementedError

    @ abstractmethod
    async def recuperar_participantes(self, id_juego: str) -> list[Participante]:
        raise NotImplementedError

    @ abstractmethod
    async def comparar_sugerencia_deseos(self, id_juego: str, id_participante: str, regalo_sugerido: str) -> ResCompararRegaloDeseos:
        raise NotImplementedError

    @ abstractmethod
    async def agregar_regalo_a_lista(self, id_juego: str, id_participante: str, regalo: str) -> ResAgregarRegalo:
        raise NotImplementedError
