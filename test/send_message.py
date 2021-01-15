from easymq.mq import MQ

mq = MQ(
    mq_user="root",
    password="root1234",
    host_and_ports=[
        ("localhost", 61613),
        ("localhost", 61613)
    ],
    queue_name="/queue/test_queue",
)

mq.send(message="123456")
