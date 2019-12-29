import time

from easymq.connect_mq import Connection, Listener


class CustomListener(Listener):

    def on_message(self, headers, message):
        print("----->", message)


if __name__ == '__main__':
    a = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], use_ssl=False, listener=CustomListener)
    while True:
        a.receive(mq_destination=["/queue/collect_event", "/queue/collect.event"])
        time.sleep(2)
