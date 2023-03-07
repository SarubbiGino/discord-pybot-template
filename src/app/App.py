from dataclasses import dataclass
from interfaces.api_interface import Api, ResAgregarParticipante, ResAgregarRegalo, ResCrearJuego, ResCompararRegaloDeseos
from interfaces.bot_interface import Bot, Contexto


@dataclass
class App:
    bot: Bot
    api: Api

    def setup(self):
        self.bot.evento_iniciar_nuevo_server(
            handler=self.iniciar_en_nuevo_servidor
        )
        self.bot.evento_iniciar_nuevo_juego(
            handler=self.iniciar_nuevo_juego
        )
        self.bot.evento_preguntan_por_amigo(
            handler=self.recuperar_amigo
        )
        self.bot.evento_comunicar_amigo_invisible(
            handler=self.enviar_a_todos_nombre_amigo
        )
        self.bot.evento_comparar_sugerencia_con_deseos(
            handler=self.comparar_regalo_sugerido_con_lista_deseos
        )
        self.bot.evento_agregar_regalo_a_lista(
            handler=self.agregar_regalo_lista_deseos
        )
        self.bot.evento_agregar_participante(
            handler=self.agregar_participante
        )

    def run(self):
        self.bot.run()
        self.api.run()

    async def iniciar_en_nuevo_servidor(self, contexto: Contexto):
        id_servidor = contexto.id_servidor
        await self.bot.dar_mensaje_bienvenida(id_servidor=id_servidor)
        await self.bot.mostrar_comandos_disponibles(id_servidor=id_servidor)

    async def iniciar_nuevo_juego(self, contexto: Contexto):
        fecha_celebracion = await self.bot.solicitar_fecha_celebracion(
            id_servidor=contexto.id_servidor
        )
        res: ResCrearJuego = await self.api.crear_nuevo_juego(
            fecha_celebracion=fecha_celebracion
        )
        if not res.fue_creado:
            await self.bot.comunicar_juego_no_fue_creado(
                id_servidor=contexto.id_servidor
            )

    async def recuperar_amigo(self, contexto: Contexto):
        nombre_amigo = await self.api.recuperar_nombre_amigo(
            id_participante=contexto.id_participante
        )
        await self.bot.enviar_nombre_amigo(
            id_participante=contexto.id_participante,
            id_servidor=contexto.id_servidor,
            nombre_amigo=nombre_amigo
        )

    async def agregar_participante(self, contexto: Contexto):
        res: ResAgregarParticipante = await self.api.agregar_particpante(
            id_juego=contexto.id_juego,
            nombre_usuario=contexto.nombre_usuario
        )
        if not res.fue_agregado:
            await self.bot.comunicar_participante_no_fue_agregado(
                id_juego=contexto.id_juego,
                nombre_usuario=contexto.nombre_usuario
            )

    async def enviar_a_todos_nombre_amigo(self, id_juego: str):
        participantes = await self.api.recuperar_participantes(
            id_juego=id_juego
        )
        await self.bot.enviar_nombre_amigo_a_todos(
            id_juego=id_juego,
            participantes=participantes
        )

    async def comparar_regalo_sugerido_con_lista_deseos(self, contexto: Contexto):
        res: ResCompararRegaloDeseos = await self.api.comparar_sugerencia_deseos(
            id_juego=contexto.id_juego,
            id_participante=contexto.id_participante,
            regalo_sugerido=contexto.regalo
        )
        await self.bot.enviar_resultados_por_sugerencia(
            id_juego=contexto.id_juego,
            id_participante=contexto.id_participante,
            resultados=res
        )
        if res.puntos_totales > 20:
            await self.mostrar_lista_deseos_amigo(
                id_juego=contexto.id_juego,
                id_participante=contexto.id_participante
            )

    async def mostrar_lista_deseos_amigo(
            self,
            id_juego: str,
            id_participante: str):
        id_amigo = await self.api.recuperar_id_amigo(
            id_juego=id_juego,
            id_participante=id_participante
        )
        lista_deseos = await self.api.recuperar_lista_deseos(
            id_juego=id_juego,
            id_participante=id_amigo
        )
        await self.bot.mostrar_lista_deseos_amigo(
            id_juego=id_juego,
            id_participante=id_participante,
            lista_deseos_amigo=lista_deseos
        )

    async def agregar_regalo_lista_deseos(self, contexto: Contexto):
        res: ResAgregarRegalo = await self.api.agregar_regalo_a_lista(
            id_juego=contexto.id_juego,
            id_participante=contexto.id_participante,
            regalo=contexto.regalo
        )
        if not res.fue_agregado:
            await self.bot.comunicar_regalo_no_fue_agregado(
                id_juego=contexto.id_juego,
                id_participante=contexto.id_participante
            )
