import json


async def parse_message(message):
    return json.loads(message.body.decode())
