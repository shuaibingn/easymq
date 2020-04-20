import logging
import threading
import stomp

event = threading.Event()


class MQListener(stomp.ConnectionListener):

    def on_message(self, headers, body):
        pass

    def on_connected(self, headers, body):
        logging.info(f"on connected: {headers}, {body}")

    def on_error(self, headers, body):
        logging.info(f"on error: {headers}, {body}")

    def on_disconnected(self):
        logging.info('on disconnected')


def wait_forever():
    event.wait()
