import cv2
import hashlib
import pickle


def video_verify(input_path):

    #open the files to check hashes with originals
    video = cv2.VideoCapture(input_path + ".mp4")
    hashfile = open(input_path + '.videohash','r')
    lasthash = "" #initial value, good for the code below, and posiibilty to add initial hash from the main network
    result = True
    while(video.isOpened()):
        ret,frame = video.read()
        if frame is None:
            break
        lasthash = hashlib.sha256((str(pickle.dumps(frame)) + lasthash).encode('utf-8')).hexdigest() #process the frame, combine hash from previous frame
        if hashfile.readline().replace('\n','') != lasthash:
            result = False
            break


    #close the hash and video files; report result
    video.release()
    hashfile.close()
    return result

video_verify("cam_video")