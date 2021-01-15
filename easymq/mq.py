import asyncio

from easymq.listener import MQListener
from easymq.log import log_control


class MQ:

    def __init__(self, mq_user, password, host_and_ports, queue_name, func=None, use_ssl=True, heartbeats=(60000, 60000)):
        self.func = func
        self.event_loop = asyncio.get_event_loop()
        self.mq_listener = MQListener(
            mq_user,
            password,
            host_and_ports,
            queue_name,
            use_ssl,
            heartbeats
        )

    @log_control
    def receive(self, logger=False):
        self.mq_listener.set_message_callback(self.message_callback)
        self.event_loop.create_task(self.mq_listener.run_forever())
        self.event_loop.run_forever()

    def message_callback(self, headers, body):
        if not self.func:
            self.mq_listener.stop()
            raise Exception("The `func` parameter is required, when receiving")

        self.func(headers, body)
        return True

    @log_control
    def send(self, message, logger=False):
        self.mq_listener.send(message)
