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

# asks user to pick overlay image
overlay = Image.open(filedialog.askopenfilename(title = "Choose overlay image"))

# function that places overlay on image(s) at certain X,Y position
def merge(files, overlay, X, Y):
    origW, origH = Image.open(files[0]).size

    # loops through image(s)
    for file in files:
        curr = Image.open(file)
        currW, currH = curr.size

        overW, overH = overlay.size

        # probably a better way to do this, but if the coordinates are decimals I assume they are percentages
        if type(X) == float:
            curr.paste(overlay, box = (int(X * (currW - overW)), int(Y * (currH - overH))), mask = overlay)
        else:
            curr.paste(overlay, box = (int(X * currW / origW - overW/2), int(Y * currH / origH - overH/2)), mask = overlay)

        file_split = file.split(".")

        # adds "Overlayed" to end of new file name
        file = "".join(file_split[:-1] + ["Overlayed"] + ["." + file_split[-1]])

        # args preserve quality in new jpeg
        curr.save(file, quality=100, subsampling=0)

    # closes all windows
    cv2.destroyAllWindows()

    # shows output image (only shows last one if multiple images)
    cv2.imshow("Output (press any key to exit)", cv2.imread(file))

    # closes output window once user presses any key
    cv2.waitKey(0)


import sys, getopt

def main(argv):
    try:
        # looks through commandline args (specifically looks for -h, -f, -m or their respective full versions)
        opts, args = getopt.getopt(argv, "hfm", ["help=", "folder=", "mouse="])
    except getopt.GetoptError:
        # returns error if any issues with args
        print('test.py <arguments> <horizontal percent> <vertical percent>')
        sys.exit(2)
    
    mouse = False
    folder = False

    # loops through args
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("test.py <horizontal percent (left = 0)> <vertical percent (top = 0)>")
            print("\t-h or --help | help")
            print("\t-f or --folder| folder (default = single file)")
            print("\t-m or --mouse | cursor select (click c to place)")
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder = True
        elif opt in ("-m", "--mouse"):
            mouse = True
    
    # asks user for file/folder depending on args
    if folder:
        folderpath = filedialog.askdirectory(title = "Choose folder of base images")
        files = [folderpath + "/" + x for x in listdir(folderpath)]
    else:
        files = [filedialog.askopenfilename(title = "Choose base image")]

    # if no mouse arg, takes in x y percentages
    if not mouse:
        values = []
        for arg in argv:
            if not "-" in arg:
                values.append(int(arg))

        # makes sure both x and y args were passed
        if len(values) != 2:
            print("test.py <arguments> <horizontal percent> <vertical percent>")
            sys.exit(2)

        percentX = int(values[0]) / 100
        percentY = int(values[1]) / 100

        merge(files, overlay, percentX, percentY)
    
    # mouse alg
    else:
        sample = cv2.imread(files[0])

        # need to declare vars global so that values can be updated by click_event()
        global img2, img3, mouseX, mouseY

        img2 = sample.copy()
        img3 = img2.copy()

        mouseX = 0
        mouseY = 0

        # function for when mouse moves: draws rectangle the size of the overlay around the cursor
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
        
        print()
        print("Press C to pick overlay position")

        # displays the image until the user picks a position by pressing "c"
        while 1:
            cv2.imshow("IMAGE",img3)
            if cv2.waitKey(20) == ord("c"):
                print(mouseX, mouseY)
                break

        merge(files, overlay, mouseX, mouseY)


if __name__ == "__main__":
    main(sys.argv[1:])