import asyncio
import logging

import stomp


class MQListener(stomp.ConnectionListener):

    def __init__(self, mq_user, password, host_and_ports, queue_name, use_ssl, heartbeats):
        self.mq_user = mq_user
        self.password = password
        self.host_and_ports = host_and_ports
        self.queue_name = queue_name
        self.use_ssl = use_ssl
        self.heartbeats = heartbeats
        self.mq_conn = self.connect()
        self._message_callback = None
        self._is_stopped = False
        self.quite_event = asyncio.Event()

    def set_message_callback(self, message_callback=None):
        self._message_callback = message_callback

    def on_message(self, headers, body):
        logging.info(f"ON_MESSAGE: {headers} {body}")

        if self._message_callback and self._message_callback(headers, body):
            self.mq_conn.ack(id=headers['message-id'], subscription=headers['subscription'])
        else:
            self.mq_conn.nack(id=headers['message-id'], subscription=headers['subscription'])

    def send(self, message: str):
        if self.mq_conn is None or not self.mq_conn.is_connected():
            self.mq_conn = self.connect()
        self.mq_conn.send(self.queue_name, message)
        logging.info(f"SEND {message} TO {self.queue_name} SUCCESS")

    def on_error(self, headers, body):
        logging.error(f"ON_ERROR: {headers} {body}")

    def stop(self):
        self._is_stopped = True
        try:
            self.mq_conn.remove_listener('ts')
        except Exception as e:
            logging.error(f"stopped error: {e}")
        self.mq_conn.running = False
        self.mq_conn.disconnect()
        self.mq_conn.stop()
        self.quite_event.set()

    def connect(self):
        try:
            conn = stomp.Connection(
                host_and_ports=self.host_and_ports,
                use_ssl=self.use_ssl,
                heartbeats=self.heartbeats
            )

            conn.set_listener('ts', self)
            conn.connect(self.mq_user, self.password, wait=True)
            conn.subscribe(destination=self.queue_name, id="0917", ack='client-individual')
            return conn
        except ConnectionRefusedError as err:
            logging.error(f'ConnectionRefusedError:{err}')
        except Exception as error:
            logging.error(f'MQ Error:{error}')

    def on_heartbeat(self):
        logging.debug('[MQListener] [ON_HEARTBEAT]')

    def on_heartbeat_timeout(self):
        logging.error('[MQListener] [LISTENER ON_HEARTBEAT_TIMEOUT]')

    def on_disconnected(self):
        logging.error('[MQListener] [LISTENER ON_DISCONNECTED]')
        if not self.mq_conn.is_connected:
            self.mq_conn = self.connect()
            logging.warning("ACTIVE MQ IS RECONNECTED")

    def ensure_connected(self):
        if self._is_stopped:
            return

        if self.mq_conn is None or not self.mq_conn.is_connected():
            self.mq_conn = self.connect()
            logging.warning("ACTIVE MQ IS CONNECTED")

    async def run_forever(self):
        while not self._is_stopped:
            self.ensure_connected()
            try:
                await asyncio.wait_for(self.quite_event.wait(), 10)
            except asyncio.TimeoutError:
                pass
        logging.error("MQListener Quit")
