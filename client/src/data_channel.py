from aiortc import RTCDataChannel, RTCDataChannelParameters

async def create_data_channel(transport):
    parameter = RTCDataChannelParameters(
        id = 2,
        label="chat-1",
        maxPacketLifeTime=10,
        maxRetransmits=None,
        negotiated=True,
        ordered=False,
        protocol=""
    )
    return RTCDataChannel(transport=transport, parameters=parameter)