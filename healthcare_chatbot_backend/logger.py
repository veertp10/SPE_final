import logging
from logstash_logback_encoder import LogstashFormatterV1

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a Logstash formatter
logstash_formatter = LogstashFormatterV1()

# Create a handler for sending logs to Logstash
logstash_handler = logging.StreamHandler()
logstash_handler.setFormatter(logstash_formatter)
# Add the handler to the logger
logger.addHandler(logstash_handler)

# Use the logger in your Flask application
logger.info('This is an info message', extra={'app': 'flask-app'})