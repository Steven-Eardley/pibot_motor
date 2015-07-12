from functools import wraps

def expect_kb_interrupt(fn):
    @wraps(fn)
    def decorated_fn(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except KeyboardInterrupt:
            pass
    return decorated_fn
