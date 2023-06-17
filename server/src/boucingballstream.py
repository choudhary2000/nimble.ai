import asyncio
from aiortc import MediaStreamTrack, VideoStreamTrack
from utils import Ball
import time
import fractions

VIDEO_CLOCK_RATE = 90000
VIDEO_PTIME = 1 / 30
VIDEO_TIME_BASE = fractions.Fraction(1, VIDEO_CLOCK_RATE)

class BouncingBallStreamTrack(MediaStreamTrack):
    kind = 'video'
    _start: float
    _timestamp: int

    def __init__(self) -> None:
        super().__init__()
        self.ball = Ball(512, 512, 10, 5, 10)

    async def next_timestamp(self):
        if hasattr(self, "_timestamp"):
            self._timestamp += int(VIDEO_PTIME * VIDEO_CLOCK_RATE)
            wait = self._start + (self._timestamp / VIDEO_CLOCK_RATE) - time.time()
            await asyncio.sleep(wait)
        else:
            self._start = time.time()
            self._timestamp = 0
        return self._timestamp, VIDEO_TIME_BASE

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        frame = self.ball.generate_frame()
        frame.pts = pts
        frame.time_base = time_base
        return frame