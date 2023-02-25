from lightning7_ssl.control_client import SSLClient

with SSLClient() as client:
    while True:
        print(client.receive())
