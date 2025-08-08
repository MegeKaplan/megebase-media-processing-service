import asyncio
from messaging.rabbitmq import init_rabbitmq, consume
from utils.parser import parse_message
from storage.minio import download_file

raw_file_path = "/tmp/raw"
processed_file_path = "/tmp/processed"

async def handle_message(message):
    async with message.process():
        message = await parse_message(message)
        download_file(message["clientId"], message["objectName"], raw_file_path)


async def main():
    queue = await init_rabbitmq()
    await consume(queue, handle_message)


if __name__ == "__main__":
    asyncio.run(main())
