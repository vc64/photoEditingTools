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
    folderpath = filedialog.askdirectory(title = "Choose folder of base images")
    files = [folderpath + "/" + x for x in listdir(folderpath)]
else:
    print("Not a valid option")


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



choice_mode = input("Percent (1) or Mouse (2): ")

if choice_mode == "1":
    print("Where do you want to place the overlay?")
    percentX = input("Enter horizontal position as percent (i.e. 0 is left edge, 100 is right edge): ")
    percentY = input("Enter vertical position as percent (i.e. 0 is top edge, 100 is bottom edge): ")

    percentX = int(percentX) / 100
    percentY = int(percentY) / 100

    merge(files, overlay, percentX, percentY)

elif choice_mode == "2":

    sample = cv2.imread(files[0])

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

    cv2.destroyAllWindows()


# import sys, getopt

# def main(argv):
#    inputfile = ''
#    outputfile = ''
#    try:
#       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#    except getopt.GetoptError:
#       print 'test.py -i <inputfile> -o <outputfile>'
#       sys.exit(2)
#    for opt, arg in opts:
#       if opt == '-h':
#          print 'test.py -i <inputfile> -o <outputfile>'
#          sys.exit()
#       elif opt in ("-i", "--ifile"):
#          inputfile = arg
#       elif opt in ("-o", "--ofile"):
#          outputfile = arg
#    print 'Input file is "', inputfile
#    print 'Output file is "', outputfile

# if __name__ == "__main__":
#    main(sys.argv[1:])