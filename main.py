import asyncio
from messaging.rabbitmq import init_rabbitmq, consume


async def handle_message(message):
    async with message.process():
        print(f"Received message: {message.body.decode()}")


async def main():
    queue = await init_rabbitmq()
    await consume(queue, handle_message)


if __name__ == "__main__":
    asyncio.run(main())
