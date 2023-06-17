import asyncio
import logging
import socket
from data_channel import create_data_channel
from aiortc import RTCPeerConnection, RTCDataChannel, RTCDataChannelParameters
from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from tcp_socket import Signaling
import multiprocessing as mp
# from aiortc.contrib.media import÷\ 
import cv2
import av
from utils import detect_ball_position
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("client.py")

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3001

class Client:
    def __init__(self, pc, signalling) -> None:
        self.pc = pc
        self.signalling = signalling
        self.queue = mp.Queue(maxsize=25)
        self._x = mp.Value("i", 0)
        self._y = mp.Value("i", 0)
        self.detect_ball_position_process = mp.Process(target=detect_ball_position, args=(self.queue, self._x, self._y, ))

    async def handle_data_channel(self):
            channel = await create_data_channel(self.pc.sctp)
            @channel.on("open")
            async def on_open():
                print("channel created", channel)

    def handle_connection_state_change(self):
        @self.pc.on("connectionstatechange")
        async def on_state_change():
            if self.pc.connectionState == "connected":
                print("connected established.")
            if self.pc.connectionState == "closed" or self.pc.connectionState == "failed":
                await self.pc.close()
            

    def handle_on_track(self):
        @self.pc.on("track")
        async def on_track(track):
            self.detect_ball_position_process.start()
            while True:
                frame = await track.recv()
                frame = frame.to_ndarray(format="bgr24")
                if not self.queue.full():
                    self.queue.put(frame)
                else:
                    LOGGER.debug("queue is full, skipping frame")
                if frame is not None:
                    cv2.imshow("Bouncing Ball", frame)
                if cv2.waitKey(1) == ord("q"):
                    break
        
    async def main(self):
        self.handle_connection_state_change()
        self.handle_on_track()
        await self.handle_data_channel()
        await self.signalling.consume_signaling()

if __name__ == "__main__":
    pc = RTCPeerConnection()
    pc.createDataChannel("hello")
    signalling = Signaling(HOST, PORT, pc)
    client = Client(pc=pc, signalling=signalling)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signalling.close())