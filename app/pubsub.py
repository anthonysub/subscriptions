import asyncio
from typing import AsyncGenerator, Any

class EventBroker:
    def __init__(self):
        # Un 'set' para guardar de forma única las colas de mensajes de todos los usuarios conectados
        self.subscribers: set[asyncio.Queue] = set()

    async def publish(self, event_type: str, data: Any):
        """
        Los Publicadores (Mutations y REST) usarán esta función.
        event_type: "CREACION", "MODIFICACION" o "ELIMINACION"
        data: Los datos del usuario afectado
        """
        mensaje = {
            "evento": event_type,
            "datos": data
        }
        # Recorremos a todos los usuarios conectados y les lanzamos el mensaje
        for queue in list(self.subscribers):
            await queue.put(mensaje)

    async def subscribe(self) -> AsyncGenerator[dict, None]:
        """
        Las Subscriptions de GraphQL usarán esta función para quedarse escuchando.
        """
        # 1. Le creamos una "bandeja de entrada" (Queue) al nuevo usuario
        queue = asyncio.Queue()
        self.subscribers.add(queue)
        
        try:
            while True:
                # 2. El código se "pausa" aquí mágicamente hasta que llegue un mensaje
                mensaje = await queue.get()
                
                # 3. 'yield' empuja el mensaje a la pantalla de GraphQL sin cerrar la conexión
                yield mensaje 
        finally:
            # 4. Si el usuario cierra el navegador, limpiamos su bandeja
            self.subscribers.remove(queue)

# Creamos UNA SOLA instancia global. Esta es la que importaremos en los demás archivos.
broker = EventBroker()