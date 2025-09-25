import cv2 #image processing
from io import BytesIO #in-memory file operations
import numpy as np #handling arrays

def process_image(image_file):
    in_memory_file = BytesIO() #storing image in our memory for temporary time
    image_file.save(in_memory_file) #saving image inside memory
    image_bytes = in_memory_file.getvalue() #fetch all contents of the image in the form of bytes
    nparr = np.frombuffer(image_bytes,np.uint8) #converting the byte data into numpy array and storing that numpy array inside np array variable
    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR) #converting numpy array into actual image that is compactible with OpenCV library
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #converting coloured image to gray scale image,(as all images in internet are bgr),grayscale are best possible images for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #pre-trained face detection model,haar cascade
    faces = face_cascade.detectMultiScale(gray,1.1,5) #detect all the faces in the grayscale image and store those inside this faces variable

    if len(faces)==0:
        return image_bytes,None #no faces found return original image and none
    
    largest_face = max(faces,key=lambda r:r[2] *r[3]) #largest face of image is detected, as (x,y,w,h) largest area is taken by multiplying width and height
    (x,y,w,h)=largest_face
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3) #rectangle boxes will be in green color
    is_sucess,buffer=cv2.imencode(".jpg",img) #encoding the image within the rectangle in jpg format

    return buffer.tobytes(),largest_face #encoded image (in bytes form), largest_face is sent