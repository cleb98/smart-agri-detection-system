import cv2
import os

counter = 0  # counter for generating unique filenames

def take_photo():
    """
    takes a photo and places it in the output folder
    """
    global counter  # make counter global so it can be incremented

    cap = cv2.VideoCapture(0) # set the camera index. '1' is for default camera 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # tune
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # tune
    ret, frame = cap.read()
    #path relativo -> os.getcwd() va in automatico al path dove c'è la folder di esecuzione di snapshot.py 
    dataset_folder = os.path.join(os.getcwd(), 'image')
    #path assoluto
    #dataset_folder = os.path.join('C:/Users/39379/Desktop/iot_project/inference iot/', 'image')


    if not os.path.exists(dataset_folder):
        print('funziona')
        os.makedirs(dataset_folder)
    

    #counter implementation 
    # generate unique filename using the counter every image will be saved in output folder
    filename = 'image/image{}.jpg'.format(counter)
    cv2.imwrite(filename, frame) # jpg/png
    counter += 1  # increment of the counter is done inside Roboflow_inference
    cap.release()
    
#uncomment it for take a photo running the script
# if __name__ == '__main__':
#     take_photo()
