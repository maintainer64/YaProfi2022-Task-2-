import logging.config
import os

LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG")
SETTINGS_LOGGER = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"()": "runner.utils.logs.JsonFormatter"}},
    "handlers": {"default": {"class": "logging.StreamHandler", "formatter": "default"}},
    "loggers": {
        "": {"level": LOGLEVEL, "handlers": ["default"]},
        "databases": {"level": "INFO", "handlers": ["default"]},
    },
}
logging.config.dictConfig(SETTINGS_LOGGER)
logging.getLogger().setLevel(LOGLEVEL)
