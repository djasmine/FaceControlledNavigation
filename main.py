import cv2
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import detect


def pose_to_direction(faces):
    if len(faces) == 0:
        return 0  # no faces detected
    pose = faces[0]["attributes"]["headpose"]
    att1 = "yaw_angle"
    att2 = "pitch_angle"
    att3 = "roll_angle"
    if pose[att1] < -3.5:
        return 1  # left
    if pose[att1] > 3.5:
        return 2  # right
    if pose[att2] < -3.5:
        return 3  # up
    if pose[att2] > 3.5:
        return 4  # down
    return 5  # no pose


def main():
    print "hello"
    video_cap = cv2.VideoCapture(0)
    video_cap.set(cv2.cv.CV_CAP_PROP_FPS, 3)
    dirs = ["no face", "left", "right", "up", "down", "front"]
    map_dirs = ["no action", Keys.LEFT, Keys.RIGHT, Keys.UP, Keys.DOWN]
    browser = webdriver.Chrome()
    browser.get("https://www.instantstreetview.com/@40.732439,-73.987242,-145.52h,5p,1z")
    elem = browser.find_element_by_class_name("widget-scene-canvas")
    elem.click()
    curr_dir = 0
    while True:
        ret, frame = video_cap.read()
        resized_img = cv2.resize(frame, (int(frame.shape[1] * 0.25), int(frame.shape[0] * 0.25)), interpolation=cv2.INTER_AREA)
        res_detect = detect.detect_face(resized_img)
        cv2.imshow('video', resized_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        result = json.loads(res_detect)
        new_dir = pose_to_direction(result["faces"])
        print dirs[new_dir]
        if new_dir == 5:
            curr_dir = 5
        elif new_dir > 0 and curr_dir == 5:
            curr_dir = new_dir
            if curr_dir == 1 or curr_dir == 2:
                elem.send_keys(map_dirs[curr_dir])
                elem.send_keys(map_dirs[curr_dir])
                elem.send_keys(map_dirs[curr_dir])
                elem.send_keys(map_dirs[curr_dir])
                elem.send_keys(map_dirs[curr_dir])
            else:
                elem.send_keys(map_dirs[curr_dir])
    video_cap.release()
    cv2.destroyAllWindows()
    browser.quit()
    print "end"


if __name__ == "__main__":
    main()
