import socket
import threading
import time
from typing import List

from lightning7_ssl.logtool.Gamelog import (
    MESSAGE_SSL_REFBOX_2013,
    MESSAGE_SSL_VISION_2010,
    MESSAGE_SSL_VISION_2014,
)

REF_ADDR = ("224.5.23.1", 10003)
VISION_ADDR = ("224.5.23.2", 10006)


class LogPlayer:
    """
    A class to play back a gamelog
    """

    speed_factor: float
    pointer: int
    header: List
    data: List
    referee: socket.socket
    vision: socket.socket

    def __init__(self, headers, data, speed_factor: float = 1.0):
        self.header = headers
        self.data = data
        self.speed_factor = speed_factor
        self.pointer = 0
        # init referee socket to send to the multicast address
        self.referee = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.referee.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        # init vision socket to send to the multicast address
        self.vision = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.vision.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def play(self, stop_event: threading.Event, start_from: int = 0, speed_factor: float = -1):
        """
        Play the gamelog
        """

        self.pointer = start_from
        if speed_factor > 0:
            self.speed_factor = speed_factor
        time_start = time.time()
        while self.pointer < len(self.header) and not stop_event.is_set():
            (timestamp, message_type, message_size) = self.header[self.pointer]
            time_relative_log = (timestamp - self.header[start_from][0]) / 1000000000.0 / self.speed_factor
            time_relative_now = time.time() - time_start
            if time_relative_log > time_relative_now:
                time.sleep(time_relative_log - time_relative_now)
            if message_type == MESSAGE_SSL_REFBOX_2013:
                self.referee.sendto(self.data[self.pointer].SerializeToString(), REF_ADDR)
            elif message_type == MESSAGE_SSL_VISION_2010 or message_type == MESSAGE_SSL_VISION_2014:
                self.vision.sendto(self.data[self.pointer].SerializeToString(), VISION_ADDR)
            self.pointer += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.referee.close()
        self.vision.close()
