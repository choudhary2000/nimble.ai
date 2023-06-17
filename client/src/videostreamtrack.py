from multiprocessing import Queue
from threading import Thread
from aiortc import VideoStreamTrack
from av import VideoFrame
import numpy as np


class BallBouncingVideoStreamTrack(VideoStreamTrack, Thread):
    def __init__(self):
        super().__init__()
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.queue = Queue(10)
    
    async def recv(self):
        img = self.queue.get()
        frame = VideoFrame.from_ndarray(img, format ="bgr24")
        pts, time_base = await self.next_timestamp()
        frame.pts = pts
        frame.time_base = time_base
        return frame