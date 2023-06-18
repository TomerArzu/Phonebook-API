import logging

from const import APP_NAME

logger = logging.getLogger(APP_NAME)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
