from settings import *

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG':    'bold_black',
                'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        }
    },
    'handlers': {
        'logfile': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': "%s/django.log" % LOG_DIR,
            'formatter': "verbose",
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
    },
    'loggers': {
        'apps.banner': {
            'handlers': ['console', 'logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}
