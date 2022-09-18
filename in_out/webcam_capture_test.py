import cv2
import pickle
from typing import List
import hashlib


class Node:
    # def __init__(self, left, right, value: str, content, is_copied=False) -> None:
    def __init__(self, left, right, value: str, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        # self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        """
        class copy function
        """
        # return Node(self.left, self.right, self.value, self.content, True)
        return Node(self.left, self.right, self.value,  True)


class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.__buildTree(values)

    def __buildTree(self, values: List[str]) -> None:

        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())  # duplicate last elem if odd number of elements
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            # return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value))

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        #content: str = f'{left.content}+{right.content}'
        # return Node(left, right, value, content)
        return Node(left, right, value)

    def printTree(self) -> None:
        self.__printTreeRec(self.root)

    def __printTreeRec(self, node: Node) -> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
                
            if node.is_copied:
                print('(Padding)')
            print("Value: "+str(node.value))
            #print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)

    def getRootHash(self) -> str:
        return self.root.value


output_path = "/Users/sergii/proof-of-video/proof-of-authenticity/cam_video"

video = cv2.VideoCapture(0)

frame_width = int(video.get(3))
frame_height = int(video.get(4))

vid_cod = cv2.VideoWriter_fourcc(*"hvc1")
output = cv2.VideoWriter(output_path + ".mp4", vid_cod, 20.0, (frame_width,frame_height))

data_block = ["d11fce82e3583f7b07d1cd9996a346ab1fc6d8e99cc0e0151be7d1f702389404"] #some init value

# a=0
while(True):
    ret,frame = video.read()
    # data = pickle.dumps(frame)
    # data_block.append(Node.hash(Node.hash(data) + data_block[-1]))
    # data_block.append((data))
    cv2.imshow("My cam video", frame)
    output.write(frame)
    if cv2.waitKey(1) &0XFF == ord('x'):
        break
    # a += 1

# close the already opened camera
video.release()
# close the already opened file
output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()

# mtree = MerkleTree(data_block)
#print("Root Hash: "+mtree.getRootHash()+"\n")

video = cv2.VideoCapture(output_path + ".mp4")

while(video.isOpened()):
    ret,frame = video.read()
    if frame is None:
        break
    data_block.append(pickle.dumps(frame))

for i in range(1, len(data_block)):
    data_block[i] = hashlib.sha256((str(data_block[i]) + data_block[i-1]).encode('utf-8')).hexdigest()

video.release()

file_chain = open(output_path + '.hashtree', 'wb') 
pickle.dump(data_block, file_chain)

