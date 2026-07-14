# Project: Titan Cloud Tech (Backend API)
# Path: core/utils/logger.py

import logging
import sys
import re

class TitanColorFormatter(logging.Formatter):
    """Кастомный форматер для КОНСОЛИ (с изолированной окраской текста уровня лога)"""
    
    COLORS = {
        'DEBUG': '\033[96m',     # Циан
        'INFO': '\033[94m',      # Синий
        'WARNING': '\033[93m',   # Желтый
        'ERROR': '\033[91m',     # Красный
        'CRITICAL': '\033[1;91m' # Жирный красный
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        colored_levelname = f"[{log_color}{record.levelname}{self.RESET}]"
        
        name_str = f" [{record.name}]" if record.name and record.name != "root" else ""
        
        format_str = (
            f"[%(asctime)s] {colored_levelname} [%(filename)s:%(lineno)d]{name_str} "
            f"%(message)s"
        )
        
        formatter = logging.Formatter(format_str, datefmt="%H:%M:%S")
        return formatter.format(record)


def get_logger(name: str = "") -> logging.Logger:
    """Создает настроенный логгер с выводом СТРОГО в консоль Docker."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Защита от дублирования логов в родительские обработчики
    logger.propagate = False

    if not logger.handlers:
        # Оставляем ТОЛЬКО консольный обработчик. 
        # Docker сам всё запишет в файлы на сервере и сделает ротацию!
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(TitanColorFormatter())
        console_handler.setLevel(logging.INFO)  
        
        logger.addHandler(console_handler)

    return logger

# Инициализация дефолтного системного логгера
logger = get_logger()