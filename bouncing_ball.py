import cv2
import numpy as np
import multiprocessing as mp
from av import VideoFrame

def generate_frames(queue):
    height, width = 480, 640
    ball_radius = 20
    ball_position = np.array([ball_radius + 10, ball_radius + 10])
    ball_velocity = np.array([2, 3])

    while True:
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        ball_position += ball_velocity
        if ball_position[0] < ball_radius or ball_position[0] > width - ball_radius:
            ball_velocity[0] *= -1
        if ball_position[1] < ball_radius or ball_position[1] > height - ball_radius:
            ball_velocity[1] *= -1

        cv2.circle(frame, tuple(ball_position), ball_radius, (0, 0, 255), -1)

        if not queue.full():
            queue.put(frame)        
        else:
            print("Queue is full, dropping frame")

        if cv2.waitKey(1) == ord("q"):
            break

    queue.put(None)

def display_frames(queue):
    while True:
        frame = queue.get()
        if frame is None:
            break

        cv2.imshow("Bouncing Ball", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    frame_queue = mp.Queue(maxsize=1000)

    frame_process = mp.Process(target=generate_frames, args=(frame_queue,))
    display_process = mp.Process(target=display_frames, args=(frame_queue,))

    frame_process.start()
    display_process.start()