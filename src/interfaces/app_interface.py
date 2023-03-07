
from dataclasses import dataclass
from datetime import date


@dataclass
class Participante:
    id_participante: str
    nombre_usuario: str
    puntos_acumulados: int
    puede_ver_deseos_amigo: bool
    id_amigo: str
    lista_deseos: list[str]


@dataclass
class Juego:
    id_juego: str
    fecha_limite_para_admitir_participantes: date
    fecha_de_inicio_del_juego: date
    fecha_de_celebracion_del_juego: date
    participantes: list[Participante]
