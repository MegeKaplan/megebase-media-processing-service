from dotenv import load_dotenv
import os

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
