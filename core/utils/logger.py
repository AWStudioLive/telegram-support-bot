# Project: Telegram Support Bot
# Path: core/utils/logger.py

import logging
import sys
import os

class ColorFormatter(logging.Formatter):
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


class CustomLogger(logging.Logger):
    """
    Кастомный логгер, который правильно определяет реальное место вызова лога.
    Пропускает файл-фасад system_logger.py, возвращая имя файла и строку хэндлера.
    """
    def findCaller(self, stack_info=False, stacklevel=1):
        f = logging.currentframe()
        if f is not None:
            f = f.f_back
        
        rv = "(unknown file)", 0, "(unknown function)", None
        
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            
            # Если лог пришел из нашего фасада, спускаемся по стеку глубже
            if filename == logging._srcfile or "system_logger.py" in filename:
                f = f.f_back
                continue
            
            rv = (co.co_filename, f.f_lineno, co.co_name, None)
            break
            
        return rv


def get_logger(name: str = "") -> logging.Logger:
    """Создает настроенный логгер с выводом СТРОГО в консоль Docker."""
    # Регистрируем наш класс, чтобы логгер использовал именно его
    logging.setLoggerClass(CustomLogger)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Защита от дублирования логов в родительские обработчики
    logger.propagate = False

    if not logger.handlers:
        # Оставляем ТОЛЬКО консольный обработчик. 
        # Docker сам всё запишет в файлы на сервере и сделает ротацию!
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        console_handler.setLevel(logging.INFO)  
        
        logger.addHandler(console_handler)

    return logger

# Инициализация дефолтного системного логгера
logger = get_logger()