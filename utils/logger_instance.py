import logging
import os

logger = logging.getLogger(os.getenv("APP_NAME"))
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
