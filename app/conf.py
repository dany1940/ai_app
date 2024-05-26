import os
from dotenv import load_dotenv


class Config():
    load_dotenv()
    POSTGRES_USER=os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB=os.getenv('POSTGRES_DB')
    POSTGRES_HOST=os.getenv('POSTGRES_HOST')
    POSTGRES_PORT=os.getenv('POSTGRES_PORT')

config = Config()
