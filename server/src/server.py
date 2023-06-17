import logging
import asyncio
import socket
from tcp_socket import Signaling
from aiortc import RTCPeerConnection
from boucingballstream import BouncingBallStreamTrack
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("server.py")

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3001

class Server:
    def __init__(self,pc, signalling):
        self.pc = pc
        self.signalling = signaling

    async def main(self):
        @self.pc.on('connectionstatechange')
        async def on_connection_state_change():
            if self.pc.connectionState == "failed" or self.pc.connectionState == "closed":
                await self.pc.close()

        @self.pc.on('datachannel')
        async def on_channel(channel):
            print(channel)
            @channel.on('message')
            async def on_message(message):
                print(message)
        await self.signalling.consume_signaling()

if __name__ == "__main__":
    pc = RTCPeerConnection()
    pc.addTrack(BouncingBallStreamTrack())
    signaling = Signaling(HOST, PORT, pc)
    server = Server(pc=pc, signalling=signaling)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(server.main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())


