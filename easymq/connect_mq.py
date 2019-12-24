import stomp
import logging


class Listener(stomp.ConnectionListener):

    def __init__(self, mq_username, mq_password, mq_destination: list, connection, listener=None, wait=False):
        self.mq_username = mq_username
        self.mq_password = mq_password
        self.mq_destination = mq_destination
        self.connection = connection
        self.listener = listener if listener else Listener
        self.wait = wait

    def on_connected(self, headers, body):
        logging.info(f"mq on connected: {headers}, {body}")

    def on_message(self, headers, message):
        pass

    def on_error(self, headers, body):
        logging.info(f"mq on error: {headers}, {body}")

    def on_disconnected(self):
        logging.info("mq on disconnected")
        self.connection.disconnect()
        c = Connection(self.mq_username, self.mq_password, self.mq_destination, self.connection, self.listener)
        c.connect(wait=self.wait)


class Connection(object):

    def __init__(self, mq_username, mq_password, host_and_ports: list, mq_destination: list, use_ssl=True, listener=None):
        self.mq_username = mq_username
        self.mq_password = mq_password
        self.mq_destination = mq_destination
        self.connection = stomp.Connection(
            host_and_ports=host_and_ports,
            use_ssl=use_ssl,
            heartbeats=(60000, 60000)
        )
        self.listener = listener if listener else Listener

    def connect(self, wait: bool):
        self.connection.set_listener("print", self.listener(self.mq_username, self.mq_password, self.mq_destination, self.connection, self.listener, wait))
        while not self.connection.is_connected():
            try:
                self.connection.start()
                self.connection.connect(self.mq_username, self.mq_password, wait=wait)
            except Exception as e:
                logging.error(f"[connect error]: {e}")
                raise e

    def send(self, message: str, wait: bool, headers=None):
        self.connect(wait=wait)
        message_sent = False
        retry_count = 0
        err = None
        while (not message_sent) and (retry_count <= 3):
            try:
                for mq in self.mq_destination:
                    self.connection.send(mq, message, headers=headers)
                    logging.info(f"[destination]: {mq}, [message]: {message}")
                self.connection.disconnect()
                message_sent = True
            except Exception as e:
                retry_count += 1
                err = e
        if not message_sent and err:
            logging.error(f"[message]: {message}, [send error]: {err}")
            raise err

    def receive(self, wait):
        self.connect(wait=wait)
        for mq in self.mq_destination:
            self.connection.subscribe(mq, "1")
