import uuid
import cv2
import threading
import queue
import time
import copy

from config import capture, body_cascade, cars2_cascade, cars_cascade, visual_interface, path_for_save
from pathlib import Path

active_cascade = cars_cascade
q_start_frame = queue.Queue()


def capture_reading(capture_content) -> None:
    """
    Method for saving frames from source video and save in queue
    :param capture_content: video from some source
    :return: None
    """
    while True:
        ret, img = capture_content.read()
        q_start_frame.put(img)
        time.sleep(1)


def find_object(cascade):
    """
    Method for looking for some objects on frames. Saves selected object on frame
    :param cascade: queue frames
    :return: None
    """
    while True:
        image_from_queue = q_start_frame.get()
        image = cv2.cvtColor(image_from_queue, cv2.COLOR_BGR2GRAY)
        found_object = cascade.detectMultiScale(image, scaleFactor=1.1, minSize=(10, 10), minNeighbors=3)
        for (x, y, w, h) in found_object:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
            crop_img = copy.deepcopy(image)
            res_image = image[y:y+h, x:x+w]
            name_image = str(uuid.uuid4()) + '.jpg'
            new_path = Path(path_for_save, name_image)
            cv2.imwrite(str(new_path), res_image)
        # if visual_interface:
        #     cv2.imshow('Test start', image)
        #     k = cv2.waitKey(30) & 0xFF
        #     if k == 27:
        #         break
        # capture.release()
        # cv2.destroyAllWindows()


read_frame = threading.Thread(target=capture_reading, args=(capture, ), daemon=True)
find_some_object = threading.Thread(target=find_object, args=(active_cascade, ), daemon=True)


if __name__ == '__main__':
    read_frame.start()
    find_some_object.start()
    print('App started. For stop app press "Esc" ')
    read_frame.join()
    find_some_object.join()
