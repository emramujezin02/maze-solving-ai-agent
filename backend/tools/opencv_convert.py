import cv2, os, numpy as np

IN = "maze_images"
OUT = "backend/data/mazes"
os.makedirs(OUT, exist_ok=True)

for f in os.listdir(IN):
    img = cv2.imread(os.path.join(IN,f),0)
    _, b = cv2.threshold(img,127,1,cv2.THRESH_BINARY_INV)
    np.savetxt(os.path.join(OUT,f.replace(".png",".txt")), b, fmt="%d")
