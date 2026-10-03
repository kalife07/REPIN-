import json
import os

from dotenv import load_dotenv

load_dotenv()

# Shared settings, stored in config.json at the project root
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

with open(CONFIG_PATH) as config_file:
    _config = json.load(config_file)

MONTH = _config['dates']['month_abbreviations']
OPTIMAL_SLEEP = _config['sleep']['optimal_hours'] #hours

# Server settings: values in the .env file override the defaults from config.json
_server = _config['server']
HOST = os.getenv('FLASK_RUN_HOST', _server['host'])
PORT = int(os.getenv('FLASK_RUN_PORT', _server['port']))
DEBUG = os.getenv('FLASK_DEBUG', str(_server['debug'])).lower() in ('true', '1', 'yes')
CORS_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ORIGINS', ','.join(_server['cors_origins'])).split(',')]
