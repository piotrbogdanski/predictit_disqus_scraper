import time


def retry(tries: int = 4, delay: int = 3, backoff: int = 1):
    """Retry calling the decorated function. Adopted from:
    https://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    :param tries: number of times to try (not retry) before giving up
    :param delay: initial delay between retries in seconds
    :param: backoff: exponential backoff
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
