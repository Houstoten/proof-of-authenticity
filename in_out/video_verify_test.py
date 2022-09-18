import cv2
import hashlib
import pickle


input_path = "/Users/sergii/proof-of-video/proof-of-authenticity/cam_video"

video = cv2.VideoCapture(input_path + ".mp4")

data_block = ["d11fce82e3583f7b07d1cd9996a346ab1fc6d8e99cc0e0151be7d1f702389404"] #some init value

while(video.isOpened()):
    ret,frame = video.read()
    if frame is None:
        break
    data_block.append(pickle.dumps(frame))


for i in range(1, len(data_block)):
    data_block[i] = hashlib.sha256((str(data_block[i]) + data_block[i-1]).encode('utf-8')).hexdigest()

video.release()

file_chain = open(input_path + '.hashtreeverif', 'wb') 
pickle.dump(data_block, file_chain)
