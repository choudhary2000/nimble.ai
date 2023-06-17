from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from aiortc import RTCSessionDescription, RTCIceCandidate

class Signaling(TcpSocketSignaling):
    def __init__(self, host, port, pc):
        super().__init__(host, port)
        self.pc = pc

    async def consume_signaling(self):
        await self.pc.setLocalDescription(await self.pc.createOffer())
        await self.send(self.pc.localDescription)
        obj = await self.receive()
        if isinstance(obj, RTCSessionDescription):
            await self.pc.setRemoteDescription(obj)
        await self.receive()
    

        # obj = await self.receive()
        # print(obj)   
        # while True:
        #     obj = await self.receive()
        #     if isinstance(obj, RTCSessionDescription):
        #         await self.pc.setRemoteDescription(obj)
        #     elif isinstance(obj, RTCIceCandidate):
        #         await self.pc.addIceCandidate(obj)
        #     elif obj is BYE:
        #         break

    async def close(self):
        return await super().close()