# FasAPIGraphQL

API con FastAPI, GraphQL y suscripciones en tiempo real.

## Suscripciones

Este proyecto incluye una suscripción de GraphQL para escuchar eventos de usuarios en vivo. La suscripción se llama `user_events` y se conecta por WebSocket en `/graphql`.

### Cómo funciona

La app usa un broker pub/sub en memoria. Cuando ocurre alguna de estas acciones, el broker publica un evento:

- `CREACION` cuando se crea un usuario
- `MODIFICACION` cuando se actualiza un usuario
- `ELIMINACION` cuando se elimina un usuario

La suscripción `user_events` se queda escuchando ese broker y envía cada evento a todos los clientes conectados sin cerrar la conexión.

### Evento que recibe el cliente

Cada mensaje llega con esta forma:

```json
{
	"evento": "CREACION",
	"datos": "..."
}
```

`evento` indica el tipo de cambio y `datos` contiene la información del usuario afectado.

### Ejemplo de suscripción

```graphql
subscription {
	userEvents: userEvents {
		evento
		datos
	}
}
```

### Qué dispara los eventos

Las mutaciones de GraphQL publican automáticamente en el broker:

- `create_user`
- `update_user`
- `delete_user`

También está configurado el router GraphQL para aceptar los protocolos de suscripción `graphql-transport-ws` y `graphql-ws`.

## Resumen

Las suscripciones sirven para notificar cambios en tiempo real a cualquier cliente conectado a GraphQL, sin hacer polling.
