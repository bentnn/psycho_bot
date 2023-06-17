from os import getenv
from aiohttp import ClientSession, BasicAuth
import logging


TOKEN: str = getenv('TOKEN')
PSYCHO_SITE_URL: str = getenv('PSYCHO_SITE_URL')
PSYCHO_SITE_REST_URL: str = f'{PSYCHO_SITE_URL}/api/v0'
PSYCHO_USER = getenv('PSYCHO_USER')
PSYCHO_PASSWORD = getenv('PSYCHO_PASSWORD')
session: ClientSession = ClientSession(auth=BasicAuth(PSYCHO_USER, PSYCHO_PASSWORD))
psycho_tests: dict = None

logging.basicConfig(format='[%(asctime)s] [%(levelname)-8s] %(message)s', level=logging.INFO)
