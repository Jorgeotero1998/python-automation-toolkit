import logging
import sys
import os
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        os.makedirs("logs/screenshots", exist_ok=True)
        
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', '%H:%M:%S')
        
        # Log a consola
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        
        # Log a archivo
        fh = logging.FileHandler("logs/automation.log")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        
    return logger

def take_error_screenshot(page, name="error"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"logs/screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path)
    return path
