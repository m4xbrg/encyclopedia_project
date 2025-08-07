import json
import logging
from pathlib import Path

class JsonFormatter(logging.Formatter):
    """Format log records as JSON with time, level and message."""
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log_entry = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname.lower(),
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)

def get_logger(name: str, *, level: int = logging.INFO, log_file: Path | None = None) -> logging.Logger:
    """Return a logger configured for JSON output.

    A stream handler is always attached. If ``log_file`` is provided, a file
    handler writing JSON lines will also be added.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = JsonFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
