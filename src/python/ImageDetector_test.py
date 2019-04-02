from ImageDetector import ImageDetector, cv2, Resolution
import time


def main() -> int:
    detector = ImageDetector(
        video_path_front=None,
        resolution_front=Resolution(1280, 720),
        in_video_front='f.mp4',
    )
    while True:
        detector.capture().detect_black_square().show()  # .save()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    detector.destroy()
    time.sleep(5)
    return 0


if __name__ == "__main__":
    main()
