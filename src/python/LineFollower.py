import cv2
import numpy as np
from collections import namedtuple
from typing import Optional  # Optional is Union with Null

Frame = Optional[np.ndarray]
Resolution = namedtuple('Resolution', ['width', 'height'])


class LineFollower:
    def __init__(self, video_path: str, resolution: Resolution = Resolution(640, 480)):
        """
        Initializes the line follower to follow the line of the given color.
        """
        self.VIDEO = cv2.VideoCapture(0)  # Video stream
        self.VIDEO.set(cv2.CAP_PROP_FRAME_WIDTH, resolution.width)
        self.VIDEO.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution.height)
        self.FCC = cv2.VideoWriter_fourcc(*'X264')
        self.OUTPUT = cv2.VideoWriter(video_path, self.FCC, 20.0, (640, 480))
        self.frame = None

        self.MIN_RED_AMOUNT = 15  # Used for erosion kernel.
        self.CONTOUR_DRAW_COLOR = (0, 255, 0)
        self.AREA_THRESHOLD = 10000  # Minimum line area.

    def save(self, frame: Frame = None):
        """
        Saves the argument frame, or self.frame if no frame was provided.
        """
        if frame is None:
            frame = self.frame
        assert frame is not None, "No frame to be saved was provided, and no frames were captured."
        self.OUTPUT.write(frame)
        return self

    def capture(self):
        """
        Blocking capture of a frame of the video, saving the output in self.frame
        """
        ret, frame = self.VIDEO.read()
        self.frame = frame
        return self

    def detectRedLine(self, frame: Frame = None):
        """
        Processes the argument frame, or self.frame if no frame was provided.
        """
        if frame is None:
            frame = self.frame
        assert frame is not None, "No frame to be processed was provided, and no frames were captured."

        # Detect red.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        h_mask = cv2.inRange(h, 0, 15) | cv2.inRange(h, 165, 180)
        s_mask = cv2.inRange(s, 50, 1000)
        v_mask = cv2.inRange(v, 50, 1000)
        mask = (h_mask & s_mask) & v_mask

        # Filter the noise.
        kernel = np.ones((self.MIN_RED_AMOUNT, self.MIN_RED_AMOUNT), np.uint8)
        red_as_white = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # # Detect the edge.
        # edges_of_red_as_white = cv2.Canny(mask, 100, 200, apertureSize=3)

        # Find the contours.
        contours, hierarchy = cv2.findContours(red_as_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Figure out the biggest one.
        biggest_contour = None
        biggest_perimeter = -1
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            if perimeter > biggest_perimeter:
                biggest_perimeter = perimeter
                biggest_contour = contour

        # Find its bounding rectangle.
        if biggest_contour is None:
            return self
        bounding_rect = np.int0(cv2.boxPoints(cv2.minAreaRect(biggest_contour)))

        # Only take a contour into account if its area is large enough.
        area = cv2.contourArea(biggest_contour)
        if area < self.AREA_THRESHOLD:
            return self

        # Find a fitted line.
        rows, cols = frame.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(biggest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
        left_y = int((-x * vy / vx) + y)
        right_y = int(((cols - x) * vy / vx) + y)

        # Add details to the frame.
        frame = cv2.line(frame, (cols - 1, right_y), (0, left_y), self.CONTOUR_DRAW_COLOR, 2)
        frame = cv2.drawContours(frame, [bounding_rect], -1, self.CONTOUR_DRAW_COLOR, 3)

        self.frame = frame  # This could be frame, red_as_white, or edges_of_red_as_white.
        return self

    def show(self, frame: Frame = None):
        """
        Shows the argument frame, or self.frame if no frame was provided.
        """
        if frame is None:
            frame = self.frame
        assert frame is not None, "No frame to be processed was provided, and no frames were captured."
        cv2.imshow('frame', frame)
        return self

    def destroy(self):
        self.VIDEO.release()
        self.OUTPUT.release()
        cv2.destroyAllWindows()
