import os

from easymq.mq import MQ

mq = MQ(
    mq_user=os.environ.get("mq_user"),
    password=os.environ.get("password"),
    host_and_ports=[
        (os.environ.get("host"), os.environ.get("port")),
    ],
    queue_name="/queue/test_queue",
)

mq.send(message="123456")
