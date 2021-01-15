# easymq
一个基于stomp的简单连接，发送和接收activemq的包

A simple package based on stomp, connection, sending and receiving ActiveMQ

# Quick Start

You can use `pip install easymq` to install easymq

[There](https://github.com/unknown-admin/easymq/tree/master/test) are two examples, send and receive message from activemq

```python
from easymq.mq import MQ


def receive(headers, body):
    print(headers, body)


mq = MQ(
    mq_user="root",
    password="root1234",
    host_and_ports=[
        ("localhost", 61613),
        ("localhost", 61613)
    ],
    func=receive,
    queue_name="/queue/test_queue",
)

mq.receive()
mq.send("12345")
```