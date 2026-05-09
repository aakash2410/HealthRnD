import time
import functools
from typing import Callable, Any
from .logger import get_logger

logger = get_logger(__name__)

def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1):
    """
    Decorator for retrying a function with exponential backoff.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f"Function '{func.__name__}' failed after {retries} retries. Exception: {e}")
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Retrying '{func.__name__}' in {sleep} seconds... (Attempt {x+1}/{retries})")
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator
