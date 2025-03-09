
import logging
from loguru import logger
import os
import sys

class LoggingConfig:
    LOG_DIR = os.path.join("logs", "logs")

    # Константы для настройки стандартного логирования
    LOGGING_CONFIG = {
        "DEBUG": f"{LOG_DIR}/logging/debug.log",
        "INFO": f"{LOG_DIR}/logging/info.log",
        "WARNING": f"{LOG_DIR}/logging/warning.log"
    }
    LOG_FORMAT = "%(asctime)s || %(name)s || %(levelname)s || %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def configure():
        # Очищаем стандартные обработчики
        logging.getLogger().handlers.clear()

        # Проверка и создание директорий для логов
        for level, file_name in LoggingConfig.LOGGING_CONFIG.items():
            log_dir = os.path.dirname(file_name)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            handler = logging.FileHandler(file_name)
            handler.setLevel(getattr(logging, level))
            handler.setFormatter(logging.Formatter(LoggingConfig.LOG_FORMAT, LoggingConfig.LOG_DATE_FORMAT))
            logging.getLogger().addHandler(handler)

        # Логи для консоли
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)  # Выводим все уровни логов в консоль
        console.setFormatter(logging.Formatter(LoggingConfig.LOG_FORMAT))
        logging.getLogger().addHandler(console)
        logging.getLogger().setLevel(logging.DEBUG)  # Общий уровень логирования


class LoguruConfig:
    LOG_DIR = os.path.join("logs", "logs")

    # Константы для настройки Loguru
    LOGURU_CONFIG = {
        "DEBUG": f"{LOG_DIR}/loguru/debug.log",
        "INFO": f"{LOG_DIR}/loguru/info.log",
        "WARNING": f"{LOG_DIR}/loguru/warning.log"
    }
    LOGURU_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> || <level>{level}</level> || {function} - {file} - {line} || <cyan>{message}</cyan>"

    @staticmethod
    def configure():
        # Удаляем все существующие обработчики Loguru
        logger.remove()

        # Настройка Loguru для записи логов по уровням
        for level, file_name in LoguruConfig.LOGURU_CONFIG.items():
            log_dir = os.path.dirname(file_name)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            logger.add(
                file_name,
                level=level,
                format=LoguruConfig.LOGURU_FORMAT,
                rotation="55 MB",
                compression='zip'
            )

        # Настройка Loguru для вывода в консоль
        logger.add(
            sys.stdout,
            level="DEBUG",  # Выводим все уровни логов в консоль
            format=LoguruConfig.LOGURU_FORMAT
        )