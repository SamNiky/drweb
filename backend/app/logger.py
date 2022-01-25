import logging
import logging.handlers


def init_logger(name):
    logger = logging.getLogger(name)
    format = '%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter(format))
    streamHandler.setLevel(logging.DEBUG)
    fileHandler = logging.handlers.RotatingFileHandler(filename='logs/app.log', maxBytes=10*1024*1024)
    fileHandler.setFormatter(logging.Formatter(format))
    fileHandler.setLevel(logging.WARN)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.debug('Logger launched')