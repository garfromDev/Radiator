import time
import functools


def filtered(delay):
  """ any function decorated with it will be
    filtred, updated only if delay is expired
  """
  def real_decorator(f):
    f.last_update = 0
    f.delay = delay
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      if time.time()-f.last_update > f.delay:
        f.last_update = time.time()
        f.value = f(*args, **kwargs)
      return f.value

    return wrapper

  return real_decorator
