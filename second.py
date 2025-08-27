import cv2
import pandas as pd
from tkinter import filedialog
import tkinter as tk

# Function to get the path of the image file using tkinter file dialog
def choose_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    return file_path

# --------------------------------------------------------------------------

# Asking the user to select an image file
img_path = choose_image()

if not img_path:
    print("No image selected. Exiting.")
    exit()

csv_path = 'colors.csv'

# reading the csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# reading the desired image from the user
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# declaring the global variables
clicked = False
r = g = b = xpos = ypos = 0

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']

    return cname
       
#The Following function to get x, y coordinates of mouse, When the User double clicks On that Part Of The Image
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)he

# Creating A Window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For the light colors, We will display the text in black color
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
