import json

from easymq.connect_mq import Connection

if __name__ == '__main__':
    a = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], use_ssl=False)
    a.send(
        mq_destination=["/queue/collect_event"],
        message=json.dumps({
            "namespace": "default",
            "__name__": "login",
            "value": 100,
            "tags": {
                "ip": "123",
                "device": "123456789",
                "user_id": "niushuaibing",
                "handler": "/api/v1/login",
                "http_code": "400"
            }
        })
    )
    a.send(mq_destination=["/queue/collect_event", "/queue/collect.event"], message="123456")
