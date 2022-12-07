import datetime
import uuid
import cv2
import threading
import queue

from config import capture, body_cascade, cars2_cascade, cars_cascade
#1 поток - собирать изображения в лист
# 2 поток работает с листом и определяет есть ли на видео человек

active_cascade = cars2_cascade
q_image = queue.Queue()


def capture_reading(capture_content):
    while True:
        ret, img = capture_content.read()
        q_image.put(img)


def find_object(cascade):
    while True:
        image_from_queue = q_image.get()
        found_object = cascade.detectMultiScale(image_from_queue, scaleFactor=1.1, minSize=(10, 10), minNeighbors=3)
        image = cv2.cvtColor(image_from_queue, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in found_object:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1, )
        name_image = str(datetime.datetime.now()) + str(uuid.uuid4())

        cv2.imshow('Test start', image)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break
    capture.release()
    cv2.destroyAllWindows()


read_image = threading.Thread(target=capture_reading, args=(capture, ), daemon=True)
find_some_object = threading.Thread(target=find_object, args=(active_cascade, ), daemon=True)


if __name__ == '__main__':
    read_image.start()
    find_some_object.start()
    print('App started. For stop app press "Esc" ')
    read_image.join()
    find_some_object.join()
