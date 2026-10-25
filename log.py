import logging
import sys


def get_logger(name: str) -> logging.Logger:
  
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)


    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
 
        logger.addHandler(console_handler)

    return logger