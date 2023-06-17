import cv2
import numpy as np
import av

class Ball:
    def __init__(self, height, width, radius, x_speed, y_speed) -> None:
        self._height = height
        self._width = height
        self._radius = radius
        self._x_speed = x_speed
        self._y_speed = y_speed
        self.position = np.array([10 + self._radius, 10 + self._radius])

    def generate_frame(self):
            frame = np.zeros([self._height, self._width, 3], dtype=np.uint8)
            self.position += np.array([self._x_speed, self._y_speed])
            if self.position[0] < self._radius or self.position[0] > self._width - self._radius:
                self._x_speed *= -1
            if self.position[1] < self._radius or self.position[1] > self._height - self._radius:
                self._y_speed *= -1
            frame = cv2.circle(frame, tuple(self.position), self._radius,  (0, 0, 255), -1)
            M = np.float32([[1, 0, 0], [0, 1, 0]])
            data_bgr = cv2.warpAffine(frame, M, (self._width, self._height))
            return av.VideoFrame.from_ndarray(data_bgr, format="bgr24")