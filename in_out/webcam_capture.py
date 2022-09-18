import cv2
import pickle
import hashlib

def webcam_capture(output_path):

    #get the video stream from device 0 (main webcam) and configure all the stuff
    video = cv2.VideoCapture(0)
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    vid_cod = cv2.VideoWriter_fourcc(*"hvc1")
    output = cv2.VideoWriter(output_path + ".mp4", vid_cod, 20.0, (frame_width,frame_height))


    #record until "X" key is hit
    #for performance reason, and lack of time in this demo we just write to file and make hash later
    while(True):
        ret,frame = video.read()
        cv2.imshow("Video capture demo. Press X to stop", frame)
        output.write(frame)
        if cv2.waitKey(1) &0XFF == ord('x'):
            break


    #close the video and file streams
    video.release()
    output.release()
    cv2.destroyAllWindows()


    #reopen the file to make hashes (since video stream was compressed it will not match to the original frames before the compression)
    video = cv2.VideoCapture(output_path + ".mp4")
    outputfile = open(output_path + '.videohash','w')
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


webcam_capture("cam_video")