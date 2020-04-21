import sys
import logging

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s:%(lineno)d:%(process)d:%(message)s",
    datefmt="%m/%d %H:%M:%S",
    level=logging.INFO
)
