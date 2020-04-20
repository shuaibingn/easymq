import threading

from easymq.connect_mq import Connection
from easymq.listener import MQListener, wait_forever


class CustomListener(MQListener):

    def on_message(self, headers, message):
        print("----->", message)


if __name__ == '__main__':
    c = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], dest="/queue/test", listener=CustomListener)
    c.receive()
    thread = threading.Thread(target=wait_forever, name="wait")
    thread.start()
