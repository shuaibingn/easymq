# easymq
一个基于stomp的简单连接，发送和接收activemq的包

A simple package based on stomp, connection, sending and receiving ActiveMQ

# Quick Start

You can use `pip install easymq` to install easymq

[There](https://github.com/unknown-admin/easymq/tree/master/test) are two examples, send and receive message from activemq

```python
from easymq.connect_mq import Connection
from easymq.listener import MQListener

# if you want send message
c = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], dest="/queue/test", use_ssl=False, listener=None)
c.send("test_message")

# if you want receive message
class CustomListener(MQListener):
    def on_message(self, headers, body):
        print(body)

c = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], dest="/queue/test", use_ssl=False, listener=CustomListener)
c.receive()
```