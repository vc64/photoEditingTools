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

print("Where do you want to place the overlay?")
percentX = input("Enter horizontal position as percent (i.e. 0 is left edge, 100 is right edge): ")
percentY = input("Enter vertical position as percent (i.e. 0 is top edge, 100 is bottom edge): ")

percentX = int(percentX) / 100
percentY = int(percentY) / 100

def merge(files, overlay, X, Y):
    origH, origW = Image.open(files[0]).size


    for file in files:
        curr = Image.open(file)
        currH, currW = curr.size

        overH, overW = overlay.size

        print((int(Y * currH), int(X * currW)))

        if type(X) == float:
            print((int(Y * currH), int(X * currW)))
            curr.paste(overlay, box = (int(X * currW), int(Y * currH)), mask = overlay)
        else:
            curr.paste(overlay, box = (int(X * currW / origW), int(Y * currH / origH)), mask = overlay)

        file_split = file.split(".")
        # print(file)
        file = "".join(file_split[:-1] + ["Overlayed"] + ["." + file_split[-1]])
        curr.save(file)


merge(files, overlay, percentX, percentY)


# def click_event(event, x, y, flags, params):
#     if event==cv2.EVENT_LBUTTONDOWN:
 
#         print(x, ' ', y)
#         # displaying the coordinates
#         # on the Shell
        
 
#         # # displaying the coordinates
#         # # on the image window
#         # font = cv2.FONT_HERSHEY_SIMPLEX
#         # b = img[y, x, 0]
#         # g = img[y, x, 1]
#         # r = img[y, x, 2]
#         # cv2.putText(img, str(b) + ',' +
#         #             str(g) + ',' + str(r),
#         #             (x,y), font, 1,
#         #             (255, 255, 0), 2)
#         # cv2.imshow('image', img)


#         merge(params[0], params[1], x, y)

#         cv2.destroyAllWindows()


# sample = cv2.imread(files[0])

# print(overlay.size, sample.shape)

# crop = [overlay.size[0]/2, (sample.shape[1] - overlay.size[0]/2 + 1), overlay.size[1]/2, (sample.shape[0] - overlay.size[1]/2 + 1)]

# print(crop)

# cv2.imshow("image", sample[int(crop[2]):int(crop[3]), int(crop[0]):int(crop[1])])

# params = [files, overlay]

# cv2.setMouseCallback('image', click_event, params)

# cv2.waitKey(0)


