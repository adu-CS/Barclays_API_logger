import logging
import json
import socket
import sys

class TCPSocketHandler(logging.Handler):
    def __init__(self, host='localhost', port=5000):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, record):
        try:
            log_entry = self.format(record)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.sendall((log_entry + "\n").encode())
            sock.close()
        except Exception as e:
            print("Failed to send log:", e)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "message": record.getMessage(),
            "level": record.levelname,
            "logger": record.name,
            "timestamp": self.formatTime(record, self.datefmt),
            "host": socket.gethostname()
        }

        # Merge in any extra metadata
        if hasattr(record, 'response_time'):
            log_record["response_time"] = record.response_time
        if hasattr(record, 'status_code'):
            log_record["status_code"] = record.status_code
        if hasattr(record, 'error'):
            log_record["error"] = record.error
        if hasattr(record, 'environment'):
            log_record["environment"] = record.environment

        return json.dumps(log_record)

def setup_logger(name, env):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        json_formatter = JsonFormatter()

        # Console handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(json_formatter)
        logger.addHandler(stream_handler)

        # TCP handler for Logstash
        tcp_handler = TCPSocketHandler()
        tcp_handler.setFormatter(json_formatter)
        logger.addHandler(tcp_handler)

    def with_extra(record_factory):
        def wrapper(*args, **kwargs):
            record = record_factory(*args, **kwargs)
            record.environment = env
            return record
        return wrapper

    logging.setLogRecordFactory(with_extra(logging.getLogRecordFactory()))

    return logger

