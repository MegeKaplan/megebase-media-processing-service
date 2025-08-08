import aio_pika
from config.settings import RABBITMQ_URL

exchange_name = "megebase.topic"
queue_name = "media_processing_queue"
routing_key = "media.file.uploaded"


async def init_rabbitmq():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.bind(exchange, routing_key)

    return queue


async def consume(queue, message_handler):
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await message_handler(message)
