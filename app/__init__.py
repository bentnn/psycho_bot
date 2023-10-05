from os import getenv
from aiohttp import ClientSession, BasicAuth
import logging


TOKEN: str = getenv('TOKEN')
PSYCHO_SITE_URL: str = getenv('PSYCHO_SITE_URL')
PSYCHO_SITE_REST_URL: str = f'{PSYCHO_SITE_URL}/api/v0'
ADMIN_ID: list = [i.strip() for i in getenv('ADMIN_ID').split(',')]
PSYCHO_USER = getenv('PSYCHO_USER')
PSYCHO_PASSWORD = getenv('PSYCHO_PASSWORD')
session: ClientSession = ClientSession(auth=BasicAuth(PSYCHO_USER, PSYCHO_PASSWORD))
psycho_tests: dict = {}
normal_test_name_to_technical: dict = {}

everyday_test_time: str = getenv('EVERYDAY_TEST_TIME', '02:07')
days_to_restart_schedule: int = int(getenv('DAYS_TO_RESTART_SCHEDULE', 7))

logging.basicConfig(format='[%(asctime)s] [%(levelname)-8s] %(message)s', level=logging.INFO)

