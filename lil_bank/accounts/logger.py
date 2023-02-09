# This is the logger.py file:

import logging
import os
import sys

from django.conf import settings

log_file = os.path.join(settings.BASE_DIR, 'logs', 'debug.log')
# debug_level = logging.INFO
# logging.basicConfig(filename=log_file, level=debug_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.INFO)


# Create a file handler
file_handler = logging.FileHandler(log_file)

# Create a formatter and set the formatter for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Add the handlers to the logger
logger.info('Logger initialized')