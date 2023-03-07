from typing import Callable

from discord import Client, Intents
from interfaces.bot_interface import Bot, Juego


class BotDiscord(Bot, Client):
    def __init__(self) -> None:
        self.handle_evento_preguntan_por_amigo: Callable = None
        Client.__init__(self, intents=Intents.all())

    def evento_preguntan_por_amigo(self, handler: Callable[[str, str], Juego]):
        self.handle_evento_preguntan_por_amigo = handler
