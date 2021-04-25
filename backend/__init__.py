from os import path

FILE_CFG_AVAILABLE = path.exists('../secrets.py')

if FILE_CFG_AVAILABLE:
    from .secrets import *
    exports = [
        "SERVER",
        "PORT",
        "DATABASE",
        "USERNAME",
        "PASSWORD",
    ]
else:
    exports = []


__all__ = exports + ['FILE_CFG_AVAILABLE']
