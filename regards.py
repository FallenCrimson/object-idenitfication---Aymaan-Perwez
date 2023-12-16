from scipy.spatial.distance import euclidean
from imutils import perspective, contours
import numpy as np
import imutils
import cv2
import tkinter as tk
from tkinter import filedialog

# Function to show array of images (intermediate results)
def show_images(images):
    for i, img in enumerate(images):
        cv2.imshow("image_" + str(i), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to get the path of the selected image using a file dialog
def get_image_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    return file_path

# Get the path of the selected image
img_path = get_image_path()

# Check if the user canceled the file dialog
if not img_path:
    print("Image selection canceled.")
    exit()

# Read image and preprocess
image = cv2.imread(img_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9, 9), 0)

edged = cv2.Canny(blur, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Sort contours from left to right as the leftmost contour is the reference object
(cnts, _) = contours.sort_contours(cnts)

# Removing The contours that are clearly not large enough
cnts = [x for x in cnts if cv2.contourArea(x) > 100]

# Here, for reference, I have used a 2-inch x 2-inch square
ref_object = cnts[0]
box = cv2.minAreaRect(ref_object)
box = cv2.boxPoints(box)
box = np.array(box, dtype="int")
box = perspective.order_points(box)
(tl, tr, br, bl) = box
dist_in_pixel = euclidean(tl, tr)
dist_in_inches = 2
pixel_per_inch = dist_in_pixel / dist_in_inches

# Drawing the remaining contours as follows
for cnt in cnts:
    box = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
    mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
    mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
    wid = euclidean(tl, tr) / pixel_per_inch
    ht = euclidean(tr, br) / pixel_per_inch
    cv2.putText(image, "{:.1f}in".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    cv2.putText(image, "{:.1f}in".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

show_images([image])
