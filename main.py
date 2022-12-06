import datetime
import uuid
import cv2
import threading
import queue

#1 поток - собирать изображения в лист
# 2 поток работает с листом и определяет есть ли на видео человек

capture = cv2.VideoCapture('http://piercam.cofairhope.com/mjpg/video.mjpg')
#capture = cv2.VideoCapture('video_test.mp4')

body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cars_cascade = cv2.CascadeClassifier('cars.xml')
cars2_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

q_image = queue.Queue()


def capture_reading(capture_content):
    while True:
        ret, img = capture_content.read()
        q_image.put(img)


def find_object(cascade):
    while True:
        image_from_queue = q_image.get()
        cars = cascade.detectMultiScale(image_from_queue, scaleFactor=1.1, minSize=(10, 10), minNeighbors=3)
        image = cv2.cvtColor(image_from_queue, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in cars:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1, )
        name_image = str(datetime.datetime.now()) + str(uuid.uuid4()) + 'car'




        cv2.imshow('Test start', image)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break
    capture.release()
    cv2.destroyAllWindows()


read_image = threading.Thread(target=capture_reading, args=(capture, ), daemon=True)
find_some_object = threading.Thread(target=find_object, args=(cars2_cascade, ), daemon=True)


if __name__ == '__main__':
    read_image.start()
    find_some_object.start()
    print('App started. For stop app press "Esc" ')
    read_image.join()
    find_some_object.join()
