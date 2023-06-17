import cv2

def detect_ball_position(queue, x, y):
    while True:
        frame = queue.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            ball_contour = max(contours, key=cv2.contourArea)
            (_x, _y), radius = cv2.minEnclosingCircle(ball_contour)
            x = int(_x)
            y = int(_y)
