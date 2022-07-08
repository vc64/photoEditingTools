from os import listdir
from PIL import Image

import tkinter as tk
from tkinter import filedialog

import cv2

root = tk.Tk()
root.withdraw()

root.attributes('-topmost', True)

print("Note: Only works with .jpg and .png, no raw files")
print()


overlay = Image.open(filedialog.askopenfilename(title = "Choose overlay image"))


choice = input("Image (1) or Folder (2): ")

if choice == "1":
    files = [filedialog.askopenfilename(title = "Choose base image")]
elif choice == "2":
    files = listdir(filedialog.askdirectory(title = "Choose folder of base images"))
else:
    print("Not a valid option")

# place = input("Where do you want to place the overlay? (Enter as X,Y): ")

def merge(files, overlay, X, Y):
    origH, origW = Image.open(files[0]).size

    for file in files:
        curr = Image.open(file)
        currH, currW = curr.size

        overH, overW = overlay.size

        curr.paste(overlay, box = (Y * currH / origH - (overH / 2.0), X * currW / origW - (overW / 2.0)), mask = overlay)

        file_split = file.split(".")
        # print(file)
        file = "".join(file_split[:-1] + ["Overlayed"] + ["." + file_split[-1]])
        curr.save(file)


def click_event(event, x, y, flags, params):
    if event==cv2.EVENT_RBUTTONDOWN:
 
        print(x, ' ', y)
        # displaying the coordinates
        # on the Shell
        
 
        # displaying the coordinates
        # on the image window
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # b = img[y, x, 0]
        # g = img[y, x, 1]
        # r = img[y, x, 2]
        # cv2.putText(img, str(b) + ',' +
        #             str(g) + ',' + str(r),
        #             (x,y), font, 1,
        #             (255, 255, 0), 2)
        # cv2.imshow('image', img)


        merge(params[0], params[1], x, y)

        cv2.destroyAllWindows()


sample = cv2.imread(files[0])

cv2.imshow("image", sample)

params = [files, overlay]

cv2.setMouseCallback('image', click_event, params)

cv2.waitKey(0)


