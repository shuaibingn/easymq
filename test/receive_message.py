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
