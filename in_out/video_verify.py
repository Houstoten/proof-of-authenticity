import cv2
import hashlib
import pickle


input_path = "cam_video"

#reopen the file to make hashes (since video stream was compressed it will not match to the original frames before the compression)
video = cv2.VideoCapture(input_path + ".mp4")
outputfile = open(input_path + '.videohashverify','w')
lasthash = "" #initial value, good for the code below, and posiibilty to add initial hash from the main network
while(video.isOpened()):
    ret,frame = video.read()
    if frame is None:
        break
    lasthash = hashlib.sha256((str(pickle.dumps(frame)) + lasthash).encode('utf-8')).hexdigest() #process the frame, combine hash from previous frame
    outputfile.write(lasthash + '\n')


#release the video stream and close the file
video.release()
outputfile.close()
