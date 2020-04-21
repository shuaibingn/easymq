import logging
import stomp
import threading

from easymq.listener import MQListener, wait_forever


class Connection(object):

    def __init__(
            self,
            mq_username: str,
            mq_password: str,
            host_and_ports: list,
            dest: str,
            use_ssl=False,
            heartbeat=(60000, 60000),
            listener=None,
            wait=True
    ):
        self.mq_username = mq_username
        self.mq_password = mq_password
        self.host_and_ports = host_and_ports
        self.dest = dest
        self.use_ssl = use_ssl
        self.heartbeat = heartbeat
        self.listener = listener if listener else MQListener
        self.wait = wait
        self.connection = stomp.Connection(
            host_and_ports=self.host_and_ports,
            use_ssl=self.use_ssl,
            heartbeats=self.heartbeat
        )
        self.connect()

    def connect(self):
        while not self.connection.is_connected():
            self.connection.set_listener(
                "default",
                self.listener()
            )
            try:
                self.connection.connect(self.mq_username, self.mq_password, wait=self.wait)
            except Exception as e:
                logging.error(f"connect error: {e}")

    def send(self, message: str, headers=None):
        try:
            self.connection.send(self.dest, message, headers=headers)
            logging.info(f"destination: {self.dest}, message: {message}")
        except Exception as e:
            logging.fatal(f"send message error with {e}")
        logging.info("send message success")

    def receive(self):
        try:
            self.connection.subscribe(self.dest, "id")
            thread = threading.Thread(target=wait_forever, name="wait")
            thread.start()
        except Exception as e:
            logging.fatal(f"receive message error with {e}")
