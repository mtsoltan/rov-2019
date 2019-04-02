import cv2
import numpy as np
from collections import namedtuple
from typing import Optional  # Optional is Union with Null

Frame = Optional[np.ndarray]
Resolution = namedtuple('Resolution', ['width', 'height'])

VERTICAL = 1
HORIZONTAL = 2


class ImageDetector:
    def __init__(self,
                 video_path_front: str = None,
                 video_path_bottom: str = None,
                 resolution_front: Resolution = Resolution(640, 480),
                 resolution_bottom: Resolution = Resolution(640, 480),
                 in_video_front=None,
                 in_video_bottom=None,
                 ):
        if in_video_front is not None:
            self.VIDEO_FRONT = cv2.VideoCapture(in_video_front)  # Video stream, defaults to 0 which is the camera.
        self.VIDEO_BOTTOM = cv2.VideoCapture(in_video_bottom)  # Video stream, defaults to 0 which is the camera.
        self.IS_REAL_TIME = isinstance(in_video_front, int)
        if self.IS_REAL_TIME:
            self.resolution_front = resolution_front
            self.VIDEO_FRONT.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_front.width)
            self.VIDEO_FRONT.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_front.height)
            self.VIDEO_BOTTOM.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_bottom.width)
            self.VIDEO_BOTTOM.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_bottom.height)
        else:
            self.resolution_front = Resolution(
                int(self.VIDEO_FRONT.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.VIDEO_FRONT.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.resolution_bottom = Resolution(
                int(self.VIDEO_BOTTOM.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.VIDEO_BOTTOM.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.FCC = cv2.VideoWriter_fourcc(*'X264')
        self.OUTPUT_FRONT = None
        if video_path_front:
            self.OUTPUT_FRONT = cv2.VideoWriter(
                video_path_front, self.FCC, 20.0, (self.resolution_front.width, self.resolution_front.height))
        self.OUTPUT_BOTTOM = None
        if video_path_bottom:
            self.OUTPUT_BOTTOM = cv2.VideoWriter(
                video_path_bottom, self.FCC, 20.0, (self.resolution_bottom.width, self.resolution_bottom.height))
        self.front_frame = None
        self.bottom_frame = None

        self.rect = None
        self.line = None
        self.state = None
        self.aspect_fixed = True
        self.direction = None

        self.MIN_RED_AMOUNT = 5  # Used for erosion kernel.
        self.AREA_THRESHOLD = 100  # Minimum line area.
        self.WALL_DISTANCE_THRESHOLD = 20  # Minimum area from the wall to consider it stuck to it.

        self.triangle_count = 0
        self.big_rectangle_count = 0
        self.small_rectangle_count = 0
        self.circle_count = 0

        self.RECT_SMALL_THRESHOLD = 5000
        self.FONT = cv2.FONT_HERSHEY_COMPLEX

    def save(self):
        if self.OUTPUT_FRONT and self.front_frame:
            self.OUTPUT_FRONT.write(self.front_frame)
        if self.OUTPUT_FRONT and self.bottom_frame:
            self.OUTPUT_FRONT.write(self.bottom_frame)
        return self

    def capture(self):
        if self.VIDEO_FRONT is not None:
            ret, frame = self.VIDEO_FRONT.read()
            self.front_frame = frame
        if self.VIDEO_BOTTOM is not None:
            ret, frame = self.VIDEO_BOTTOM.read()
            self.bottom_frame = frame
        return self

    def find_direction(self, rect=None, line=None):
        """
        Finds the initial direction the robot should face.
        Takes the rectangle bounding the red line,
        and the line passing through the red line as arguments.
        """
        if rect is None:
            rect = self.rect
        if line is None:
            line = self.line

        touching_wall_l = False
        touching_wall_r = False
        touching_wall_t = False
        touching_wall_b = False
        for coord in rect:
            wall_l = coord[0]
            wall_r = self.resolution_front.width - coord[0]
            wall_t = coord[1]
            wall_b = self.resolution_front.height - coord[1]
            touching_wall_l = touching_wall_l or (wall_l < self.WALL_DISTANCE_THRESHOLD)
            touching_wall_r = touching_wall_r or (wall_r < self.WALL_DISTANCE_THRESHOLD)
            touching_wall_t = touching_wall_t or (wall_t < self.WALL_DISTANCE_THRESHOLD)
            touching_wall_b = touching_wall_b or (wall_b < self.WALL_DISTANCE_THRESHOLD)

        rect_width = pow(
            pow(rect[0][0] - rect[1][0], 2) +
            pow(rect[0][1] - rect[1][1], 2), 0.5)
        rect_height = pow(
            pow(rect[1][0] - rect[2][0], 2) +
            pow(rect[1][1] - rect[2][1], 2), 0.5)

        aspect_ratio = max(rect_width, rect_height) / min(rect_width, rect_height)

        [vx, vy, _, _] = line
        angle = int(np.math.degrees(np.math.atan(vy / vx)) % 180)

        def recognize_direction(extra_cond_h: bool = True, extra_cond_v: bool = True) -> Optional[str]:
            if touching_wall_l and not touching_wall_r and extra_cond_h:
                self.state = HORIZONTAL
                return 'a'
            if touching_wall_r and not touching_wall_l and extra_cond_h:
                self.state = HORIZONTAL
                return 'd'
            if touching_wall_t and not touching_wall_b and extra_cond_v:
                self.state = VERTICAL
                return 'u'
            if touching_wall_b and not touching_wall_t and extra_cond_v:
                self.state = VERTICAL
                return 'j'
            return None

        state = None
        if 60 < angle < 120:
            state = VERTICAL
        if angle < 30 or angle > 150:
            state = HORIZONTAL
        if self.state is None and state is not None:
            self.state = (state == VERTICAL) and HORIZONTAL or VERTICAL
            self.direction = recognize_direction()
            # print(self.direction)

        if self.state is None:
            return self

        if aspect_ratio < 2 and self.aspect_fixed:
            self.direction = recognize_direction(self.state == VERTICAL, self.state == HORIZONTAL)
            # print(self.direction)
            if self.direction is not None:
                self.aspect_fixed = False

        if aspect_ratio > 3:
            self.aspect_fixed = True

        return self

    def detect_red_line(self):
        frame = self.front_frame
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
        self.rect = np.int0(cv2.boxPoints(cv2.minAreaRect(biggest_contour)))

        # Only take a contour into account if its area is large enough.
        area = cv2.contourArea(biggest_contour)
        if area < self.AREA_THRESHOLD:
            return self

        # Find a fitted line.
        rows, cols = frame.shape[:2]
        self.line = cv2.fitLine(biggest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
        [vx, vy, x, y] = self.line
        left_y = int((-x * vy / vx) + y)
        right_y = int(((cols - x) * vy / vx) + y)

        # Add details to the frame.
        frame = cv2.line(frame, (cols - 1, right_y), (0, left_y), (0, 255, 0), 2)
        frame = cv2.drawContours(frame, [self.rect], -1, (0, 255, 0), 3)

        self.front_frame = frame  # This could be frame, red_as_white, or edges_of_red_as_white.
        return self

    def detect_shapes(self):
        frame = self.bottom_frame
        assert frame is not None, "No frame to be processed was provided, and no frames were captured."

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        x, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, y = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours_triangle = []
        contours_small_rectangle = []
        contours_big_rectangle = []
        contours_circle = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            # x = approx.ravel()[0]
            # y = approx.ravel()[1]

            if len(approx) == 3:
                self.triangle_count += 1
                contours_triangle.append(approx)
            elif len(approx) == 4:
                res_area = (self.resolution_bottom.width - 10) * (self.resolution_bottom.height - 10)
                if cv2.contourArea(cnt) > res_area:
                    continue
                if cv2.contourArea(cnt) > self.RECT_SMALL_THRESHOLD:
                    self.big_rectangle_count += 1
                    contours_big_rectangle.append(approx)
                else:
                    self.small_rectangle_count += 1
                    contours_small_rectangle.append(approx)
            else:
                self.circle_count += 1
                contours_circle.append(approx)

        color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        color = cv2.drawContours(color, contours_triangle, -1, (0, 255, 0), 3)
        color = cv2.drawContours(color, contours_small_rectangle, -1, (0, 0, 255), 3)
        color = cv2.drawContours(color, contours_big_rectangle, -1, (0, 255, 255), 3)
        color = cv2.drawContours(color, contours_circle, -1, (255, 0, 255), 3)
        self.bottom_frame = color
        return self

    def show(self):
        if self.front_frame is not None:
            cv2.imshow('front_frame', self.front_frame)
        if self.bottom_frame is not None:
            cv2.imshow('bottom_frame', self.bottom_frame)
        return self

    def reset_front(self):
        self.rect = None
        self.line = None
        self.state = None
        self.aspect_fixed = True
        self.direction = None
        return self

    def reset_bottom(self):
        self.triangle_count = 0
        self.big_rectangle_count = 0
        self.small_rectangle_count = 0
        self.circle_count = 0
        return self

    def destroy(self):
        if self.VIDEO_FRONT is not None:
            self.VIDEO_FRONT.release()
        if self.VIDEO_BOTTOM is not None:
            self.VIDEO_BOTTOM.release()
        if self.OUTPUT_FRONT is not None:
            self.OUTPUT_FRONT.release()
        if self.OUTPUT_BOTTOM is not None:
            self.OUTPUT_BOTTOM.release()
        cv2.destroyAllWindows()
