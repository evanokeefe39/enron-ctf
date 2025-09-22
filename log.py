
import logging
import sys

def get_logger(name='__name__', log_file=None):
    """
    Configure and return a logger that outputs to stdout and optionally a file.
    
    Args:
        name (str): Name of the logger (default: __name__).
        log_file (str): Path to the log file (default: 'duckdb_log.log'). Set to None to disable.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if logger is reused
    if not logger.handlers:
        # Formatter for pretty output
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # Handler for stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
        
        # Handler for file (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger