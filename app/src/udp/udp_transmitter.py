import datetime
import logging
import socket
import threading
import time

import requests  # type: ignore

from src.can.can_listeners import UdpPayloadListener
from src.util import config


class UdpTransmitter:
    UDP_INTERVAL_TIME = 0.030

    machineId: int
    runId: int
    errorCode: int

    udpSocket: socket.socket
    thread: threading.Thread
    udpPayloadListener: UdpPayloadListener

    def __init__(self, udpPayloadListener: UdpPayloadListener) -> None:
        self.udpPayloadListener = udpPayloadListener
        self.machineId = config.machineId
        self.udpAddress = config.udpAddress
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super().__init__()

    def __del__(self):
        self.udpSocket.close()

    def trySend(self):
        try:
            payload = self.udpPayloadListener.getUdpPayload(
                self.machineId, self.runId, 0
            )
            self.udpSocket.sendto(payload, self.udpAddress)
        except BaseException:
            logging.error("UDP send failed!")

    def sendEvery(self):
        baseTime = time.time()
        while True:
            # 処理を別スレッドで実行する
            t = threading.Thread(target=self.trySend)
            t.start()

            # 基準時刻と現在時刻の剰余を元に、次の実行までの時間を計算する
            now = time.time()
            elapsedTime = now - baseTime
            sleep_sec = self.UDP_INTERVAL_TIME - (elapsedTime % self.UDP_INTERVAL_TIME)

            time.sleep(max(sleep_sec, 0))

    def initialize(self):
        self.runId = getRunId(
            self.machineId, datetime.datetime.now(datetime.timezone.utc)
        )

    def run(self):
        self.initialize()
        self.sendEvery()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.setDaemon(True)
        self.thread.start()


def getRunId(machineId: int, dt: datetime.datetime) -> int:  # dt は UTCを渡す
    url = config.cloudRunApiEndpoint
    data = {"start_at": dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "machine_id": machineId}
    while True:
        try:
            res = requests.post(url, json=data)
            if res.status_code == 200:
                runId = res.json()["run"]["id"]
                logging.info(f"Run ID: {runId}")
                return runId
            else:
                raise BaseException
        except BaseException:
            time.sleep(1)
