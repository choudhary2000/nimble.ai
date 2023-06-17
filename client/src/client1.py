
class Client(TcpSocketSignaling):
    def __init__(self):
        super().__init__(HOST, PORT)
        self.pc = RTCPeerConnection()

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
                print("Exiting")
                break


    # async def handle_signalling(self):
    #     offer = await self.receive()
    #     await self.pc.setRemoteDescription(offer)
    #     answer = await self.pc.createAnswer()
    #     await self.pc.setLocalDescription(answer)
    #     await self.send(answer)
    #     while True:
    #         obj = await self.receive()
    #         if isinstance(obj, RTCIceCandidate):
    #             await self.pc.addIceCandidate(obj)
    #         elif obj is BYE:
    #             break

    async def handle_datachannel(self):
        channel = self.pc.createDataChannel("hello")
        async def send_ping():
            while True:
                channel.send("Hello")
                await asyncio.sleep(1)

        @channel.on("open")
        def on_open():
            asyncio.ensure_future(send_ping())

    async def run(self):
        await self.handle_datachannel()
        await self.consume_signaling()
        

if __name__ == "__main__":
    client = Client()


    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()