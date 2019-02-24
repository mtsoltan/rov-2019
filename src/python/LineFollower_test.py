from LineFollower import LineFollower, cv2, Resolution
import time


def main() -> int:
    follower = LineFollower(f'output{time.time()}.avi', Resolution(1280, 720))
    while True:
        follower.capture().detectRedLine().show()  # .save()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    follower.destroy()
    time.sleep(5)
    return 0


if __name__ == "__main__":
    main()
