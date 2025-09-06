import logging
from config import EnviromentOption, settings
from .loggers.stdout_formatter import StdoutFormatter
from .loggers.file_formatter import FileFormatter


MAX_FILE_STORE_LOGFILE = 5
MAX_SIZE_STORE_LOGFILE = 10485760  # 10M


class Logger:

    def __init__(
        self,
        name: str = __name__,
        level: int = logging.DEBUG,
        filename: str = "app.log",
    ):
        self.filename = filename

        self.logger = logging.getLogger(name)
        self.logger.propagate = True
        self.logger.setLevel(level)

        self.logger.handlers = [
            self._store_to_file(),
        ]

        if settings.APP_ENV == EnviromentOption.DEVELOPMENT.value:
            self.logger.handlers.append(self._stdout())

    def _stdout(self):
        handler = logging.StreamHandler()
        handler.setFormatter(StdoutFormatter())

        return handler

    def _store_to_file(self):
        handler = FileFormatter(
            fmt=None,
            filename=self.filename,
            max_size_store_logfile=MAX_SIZE_STORE_LOGFILE,
            max_file_store_logfile=MAX_FILE_STORE_LOGFILE,
        )

        return handler.handler()

    def __getattr__(self, name):
        if hasattr(self.logger, name):
            return lambda message, **kwargs: getattr(self.logger, name)(
                message, extra=kwargs.get("extra", {})
            )

        raise AttributeError(f"'{self.__class__.__name__}' has not function '{name}'")
