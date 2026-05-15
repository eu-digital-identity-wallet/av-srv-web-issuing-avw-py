import logging
import os
from concurrent_log_handler import ConcurrentTimedRotatingFileHandler



class WerkzeugFilter(logging.Filter):
    def filter(self, record):
        if "HTTP/1" in record.getMessage():
            return False
        return True


def configure_logging(app, config):
    """
    Configures logging for Flask, Werkzeug, and Gunicorn.

    :param app: The Flask application instance.
    :param config: The configuration dictionary.
    """
    log_file_path = config["log_dir"]
    log_level = getattr(logging, config.get("log_level", "INFO").upper(), logging.INFO)

    log_dir = os.path.dirname(log_file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    log_formatter = logging.Formatter(
        '%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s'
    )

    file_handler = ConcurrentTimedRotatingFileHandler(
        filename=log_file_path,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)

    # Sync with Gunicorn's level if it's more specific than what config says
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger.level != logging.NOTSET:
        log_level = gunicorn_logger.level

    loggers_to_configure = [
        logging.getLogger(),
        app.logger,
        logging.getLogger('werkzeug'),
        logging.getLogger('gunicorn.error'),
        logging.getLogger('gunicorn.access'),
    ]

    for logger in loggers_to_configure:
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(log_level)
        logger.propagate = False

    logging.getLogger('werkzeug').addFilter(WerkzeugFilter())

    app.logger.info("Logging initialized. Outputting to console and %s", log_file_path)