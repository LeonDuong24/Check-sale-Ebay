
import functools
import time
import traceback
from main import logger
def retry(max_attempts, retry_interval):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    # Thực hiện hàm gốc
                    result = func(*args, **kwargs)
                    break
                except Exception as e:
                    if attempt+1==max_attempts:
                        logger.error(traceback.format_exc())
                    attempt += 1
                    time.sleep(retry_interval)
            return result

        return wrapper_retry

    return decorator_retry
