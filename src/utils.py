from socket import AF_INET, SOCK_STREAM, socket


def find_free_port():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


def is_port_in_use(port):
    with socket(AF_INET, SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
