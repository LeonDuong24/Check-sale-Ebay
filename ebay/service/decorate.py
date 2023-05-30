
import functools
import time

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
                    attempt += 1
                    time.sleep(retry_interval)
            return result

        return wrapper_retry

    return decorator_retry
