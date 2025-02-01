import os, yaml
from log_logic import setup_logger
from aiogram.types import ReactionTypeEmoji

_consts = None

with open('settings.yaml', 'rb') as f: 
    _consts: dict = yaml.full_load(f)['settings']

from log_logic import setup_logger
BOT_NAME = _consts.get('BOT_NAME', "SOMEBOT")
LOGGER_SETTINGS = _consts.get('LOGS')
LOGS_URL, LOGS_LOGIN, LOGS_PASSWORD = None, None, None
if LOGGER_SETTINGS:
    LOGS_URL = LOGGER_SETTINGS.get('LOGS_URL', 'ws://localhost:8888/logpipe')
    LOGS_LOGIN = LOGGER_SETTINGS.get('LOGS_LOGIN', '')
    LOGS_PASSWORD = LOGGER_SETTINGS.get('LOGS_PASSWORD', '')

logger = setup_logger(name=BOT_NAME, filepath = './logs/latest.log',
                       logserver_url= LOGS_URL,
                       password = LOGS_PASSWORD,
                       username = LOGS_LOGIN)

BOT_TOKEN = _consts.get('BOT_TOKEN')

REACTION_OK = [ReactionTypeEmoji(emoji="👀")]
REACTION_UNKNOWN = [ReactionTypeEmoji(emoji="🤨")]
