
from loguru import logger
from pathlib import Path


def write_dotenv(env:str):
    logger.debug(f"------Setting up environment!----")
    logger.debug(f"------copying .env.{env} to .env file----")

    root = Path(__file__).parent.parent

    copyFrom = root.with_name(f".env.{env}")
    copyTo = root.with_name(".env")
    
    with open(copyFrom, "r", encoding = 'utf-8') as input:
        with open(copyTo, 'w', encoding = 'utf-8') as output:
            for line in  input:
                output.write(line)


def dev():
    write_dotenv(env="dev")

def prod():
    write_dotenv(env="prod")

def test():
    write_dotenv(env="test")

