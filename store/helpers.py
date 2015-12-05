import socket
import platform


def get_host_name():
    return platform.uname()[1]


def get_host_ip():
    hostname = get_host_name()
    return socket.gethostbyname(hostname)
