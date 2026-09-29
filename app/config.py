import os

from dotenv import load_dotenv

load_dotenv()

MONTH = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
OPTIMAL_SLEEP = 8.5 #hours

# Server settings, read from the .env file (defaults are used when a value is missing)
HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() in ('true', '1', 'yes')
CORS_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ORIGINS', '*').split(',')]
