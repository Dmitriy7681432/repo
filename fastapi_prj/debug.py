import time
def retry(max_retries):
    def retry_decorator(func):
        def _wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    func(*args, **kwargs)
                except:
                    time.sleep(1)
        return _wrapper
    return retry_decorator


@retry(4)
def might_fail():
    print("might_fail")
    raise Exception


might_fail()

dict_bin = {'stream': 'bnbusdt@aggTrade', 'data': {'e': 'aggTrade', 'E': 1769173069043, 'a': 798623311, 's': 'BNBUSDT', 'p'
: '888.350', 'q': '0.02', 'nq': '0.02', 'f': 2011660250, 'l': 2011660250, 'T': 1769173068889, 'm': False}}