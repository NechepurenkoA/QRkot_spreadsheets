import logging

FILE_LOCATION_ROUTE = 'app/logger/logs.txt'
LINES_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(FILE_LOCATION_ROUTE, mode='w', encoding='utf-8')
log_formatter = logging.Formatter(LINES_FORMAT)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
