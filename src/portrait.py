import cv2

def extract_portrait(image_path):
    #load the pic
    img= cv2.imread(image_path)

    #haar cascade
    #convert to BLCK&WHT
    imgblckwht = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_cascade.detectMultiScale(imgblckwht, scaleFactor=1.1, minNeighbors=5)

    if len(face) == 0:
        raise ValueError("No faces detected in the image.")

    #pick the lragest face (incase multiple faces are detected)
    largest_face = max(face, key=lambda rect: rect[2] * rect[3])  # rect is (x, y, w, h)
    x, y, w, h = largest_face
    #crop the image to the face
    portrait = img[y:y+h, x:x+w]
    return portrait

if __name__ == "__main__":
    portrait = extract_portrait("../research/sample_card.jpg")
    if portrait is not None:
        cv2.imwrite("test_portrait.png", portrait) #imwrite saves the image to disk
        print("Portrait saved!")
    else:
        print("No face found!")