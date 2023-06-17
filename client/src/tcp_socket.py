from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from aiortc import RTCSessionDescription, RTCIceCandidate

class Signaling(TcpSocketSignaling):
    def __init__(self, host, port, pc):
        super().__init__(host, port)
        self.pc = pc

    async def consume_signaling(self):
        while True:
            obj = await self.receive()
            if isinstance(obj, RTCSessionDescription):
                await self.pc.setRemoteDescription(obj)
                if obj.type == "offer":
                    await self.pc.setLocalDescription(await self.pc.createAnswer())
                    await self.send(self.pc.localDescription)
            elif isinstance(obj, RTCIceCandidate):
                await self.pc.addIceCandidate(obj)
            elif obj is BYE:
                break

    async def close(self):
        return await super().close()
    
            