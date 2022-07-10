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

# img2 = ""
# img3 = ""


def merge(files, overlay, X, Y):
    origW, origH = Image.open(files[0]).size


    for file in files:
        curr = Image.open(file)
        currW, currH = curr.size

        overW, overH = overlay.size

        if type(X) == float:
            curr.paste(overlay, box = (int(X * (currW - overW)), int(Y * (currH - overH))), mask = overlay)
        else:
            curr.paste(overlay, box = (int(X * currW / origW - overW/2), int(Y * currH / origH - overH/2)), mask = overlay)

        file_split = file.split(".")
        # print(file)
        file = "".join(file_split[:-1] + ["Overlayed"] + ["." + file_split[-1]])
        curr.save(file, quality=100, subsampling=0)

    cv2.destroyAllWindows()

    cv2.imshow("Output", cv2.imread(file))

    cv2.waitKey(0)


import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hfm", ["folder=", "mouse="])
    except getopt.GetoptError:
        print('test.py <arguments> <horizontal percent> <vertical percent>')
        sys.exit(2)
    mouse = False
    folder = False
    for opt, arg in opts:
        if opt == '-h':
            print("test.py <horizontal percent (left = 0)> <vertical percent (top = 0)>")
            print("\t-h | help")
            print("\t-f | folder (default = single file)")
            print("\t-m | cursor select (click c to place)")
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder = True
        elif opt in ("-m", "--mouse"):
            mouse = True
    
    if folder:
        folderpath = filedialog.askdirectory(title = "Choose folder of base images")
        files = [folderpath + "/" + x for x in listdir(folderpath)]
    else:
        files = [filedialog.askopenfilename(title = "Choose base image")]


    if not mouse:
        values = []
        for arg in argv:
            if not "-" in arg:
                values.append(int(arg))
        
        if len(values) != 2:
            print("test.py <arguments> <horizontal percent> <vertical percent>")
            sys.exit(2)

        percentX = int(values[0]) / 100
        percentY = int(values[1]) / 100

        merge(files, overlay, percentX, percentY)
    
    else:
        sample = cv2.imread(files[0])
        global img2, img3, mouseX, mouseY

        img2 = sample.copy()
        img3 = img2.copy()

        mouseX = 0
        mouseY = 0

        def click_event(event,x,y,flags,param):
            global img2,img3, mouseX, mouseY

            if event == cv2.EVENT_MOUSEMOVE:
                img3 = img2.copy()
                offsetX = int(param[1].size[0]/2)
                offsetY = int(param[1].size[1]/2)

                cv2.rectangle(img3,(x-offsetX, y-offsetY),(x+offsetX, y+offsetY),(255,0,0),2)
            mouseX = x
            mouseY = y


        cv2.namedWindow('IMAGE')

        params = [files, overlay]
        cv2.setMouseCallback('IMAGE', click_event, params)
        while 1:
            cv2.imshow("IMAGE",img3)
            if cv2.waitKey(20) == ord("c"):
                print(mouseX, mouseY)
                break

        merge(files, overlay, mouseX, mouseY)


if __name__ == "__main__":
    main(sys.argv[1:])