import logging
import stomp


class Listener(stomp.ConnectionListener):

    def on_connected(self, headers, body):
        logging.info(f"[mq on connected]: {headers}, {body}")

    def on_message(self, headers, body):
        pass

    def on_error(self, headers, body):
        logging.info(f"[mq on error]: {headers}, {body}")

    def on_disconnected(self):
        logging.info("[mq on disconnected]")


class Connection(object):

    def __init__(self, mq_username, mq_password, host_and_ports: list, dest: str, use_ssl=False,
                 heartbeat=(60000, 60000), listener=None, wait=True):
        self.mq_username = mq_username
        self.mq_password = mq_password
        self.host_and_ports = host_and_ports
        self.dest = dest
        self.use_ssl = use_ssl
        self.heartbeat = heartbeat
        self.listener = listener if listener else Listener
        self.wait = wait
        self.connection = stomp.Connection(host_and_ports=self.host_and_ports, use_ssl=self.use_ssl, heartbeats=self.heartbeat)
        self.connect()

    def connect(self):
        while not self.connection.is_connected():
            self.connection.set_listener("print", self.listener())
            try:
                self.connection.connect(self.mq_username, self.mq_password, wait=self.wait)
            except Exception as e:
                logging.error(f"[connect error]: {e}")

    def send(self, message: str, headers=None):
        message_status = False
        retry_count = 0
        err = None
        while not message_status and retry_count <= 3:
            try:
                self.connection.send(self.dest, message, headers=headers)
                logging.info(f"[destination]: {self.dest}, [message]: {message}")
                message_status = True
            except Exception as e:
                retry_count += 1
                err = e
        if not message_status and err:
            logging.error(f"message error with {err}")
            return err
        logging.info("send message success")

    def receive(self, mq_destination: list):
        pass
