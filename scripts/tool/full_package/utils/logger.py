# utils/logger.py
import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger('FileTracker')
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler('file_tracker.log')
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = setup_logger()