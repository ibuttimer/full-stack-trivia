from os import path

# Check if running from backend folder or backend/flasker
basedir = path.abspath(path.dirname(__file__))

FILE_CFG_AVAILABLE = path.exists(f'{basedir}/secrets.py')

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
