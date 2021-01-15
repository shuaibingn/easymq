import os

from easymq.mq import MQ


def receive(headers, body):
    print("---->", body)


mq = MQ(
    mq_user=os.environ.get("mq_user"),
    password=os.environ.get("password"),
    host_and_ports=[
        (os.environ.get("host"), os.environ.get("port")),
    ],
    func=receive,
    queue_name="/queue/test_queue",
)

mq.receive()
