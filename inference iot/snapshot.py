import cv2
import os

def take_photo():
    """
    takes a photo and places it in the output folder
    """
    cap = cv2.VideoCapture(0) # set the camera index. '1' is for default camera 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # tune
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # tune
    ret, frame = cap.read()
    dataset_folder = os.path.join(os.getcwd(),'output')
    

    if not os.path.exists(dataset_folder):
        print('funziona')
        os.makedirs(dataset_folder)
        
    # cv2.imwrite('output/image.jpg', frame) # jpg/png
    cv2.imwrite('image.jpg', frame) # jpg/png

    cap.release()

if __name__ == '__main__':
    try:
        take_photo()
    except Exception as e:
        print('You cannot take a photo!', e)
