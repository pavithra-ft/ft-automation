import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.DEBUG):
    """

    :param name: Name of the Logger
    :param log_file: Log file name
    :param level: Level of logger
    :return: app_logger/sql_logger will be set to the specified level of logging
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


app_logger = setup_logger('application_logger', 'application.log')
sql_logger = setup_logger('sql_queries_logger', 'sql_queries.log')
