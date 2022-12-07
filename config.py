import cv2
from pathlib import Path

capture = cv2.VideoCapture('http://piercam.cofairhope.com/mjpg/video.mjpg')
#capture = cv2.VideoCapture('video_test.mp4')

body_cascade = cv2.CascadeClassifier(str(Path('cascades', 'haarcascade_fullbody.xml')))
cars_cascade = cv2.CascadeClassifier(str(Path('cascades', 'cars.xml')))
cars2_cascade = cv2.CascadeClassifier(str(Path('cascades', 'haarcascade_car.xml')))
