from easymq.connect_mq import Connection

if __name__ == '__main__':
    a = Connection(mq_username="admin", mq_password="admin", host_and_ports=[("localhost", 61613)], dest="/queue/test")
    a.send(message="123456")
