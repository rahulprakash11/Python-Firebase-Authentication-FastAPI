import subprocess
from loguru import logger


def dev():
    logger.debug(
        f"------running dev!----"
    )
    cmd1='copy .env.dev .env'
    subprocess.run(['powershell','-command',cmd1])
    logger.info(
        f"------Copying .env.dev into .env file!----"
    )

    # cmd2='(poetry run serve-uvicorn)'
    cmd2='(python serve_uvicorn.py)'
    subprocess.run(['powershell','-command',cmd2])
    logger.info(
        f"------Copying .env.dev into .env file!!!!----"
    )


def prod():
    cmd1='copy .env.prod .env'
    subprocess.run(['powershell','-command',cmd1])
    logger.info(
        f"------Copying .env.prod into .env file!----"
    )

    cmd2='(python serve_uvicorn.py)'
    subprocess.run(['powershell','-command',cmd2])