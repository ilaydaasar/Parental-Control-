import cv2

def blur_image(path):
    img = cv2.imread(path)
    return cv2.GaussianBlur(img, (99, 99), 30)
