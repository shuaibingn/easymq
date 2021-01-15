from easymq.mq import MQ


def receive(headers, body):
    print("---->", body)


mq = MQ(
    mq_user="portfolio",
    password="kingsoft1116",
    host_and_ports=[
        ("b-8ba779ce-36a1-4eca-aca9-776d8d7df359-1.mq.us-west-2.amazonaws.com", 61614),
        ("b-8ba779ce-36a1-4eca-aca9-776d8d7df359-2.mq.us-west-2.amazonaws.com", 61614)
    ],
    func=receive,
    queue_name="/queue/test_queue",
)

mq.receive()
