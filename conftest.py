import os

# ignore async loop warning in order to use playwright

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")