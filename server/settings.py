import os

environment = os.getenv("ENV_NAME", "hello")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(asctime)s %(levelname)s %(filename)s] -- %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console']},
}

