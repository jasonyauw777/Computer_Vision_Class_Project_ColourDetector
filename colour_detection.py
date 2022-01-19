import numpy as np 
import pandas as pd
import cv2

## READING TEST IMAGE (5 test images)

# test_img = cv2.imread("rainbow.jpeg")
test_img = cv2.imread("Floating_Ice_Cream.jpg")
# test_img = cv2.imread("JC_Dunk.jpg")
# test_img = cv2.imread("John_Wick.jpg")
# test_img = cv2.imread("Thomas_Edison.jpg")

## RESIZING TEST IMAGE
dim = (700,500)
test_img = cv2.resize(test_img, dim)

## READING colors.csv file
## Adding column names
## CSV file contains colour name, hex code, RGB values
index=["colour", "colour_name", "hex", "R", "G", "B"]
colours_df = pd.read_csv('colors.csv', names=index, header=None)

## Creating Global Variables
clicked = False
r = g = b = xpos = ypos = 0

## USE KNN ALGORITHM TO PREDICT COLOUR 
def recognize_colour(R,G,B):
    minimum = 10000
    for i in range(len(colours_df)):
        d = abs(R- int(colours_df.loc[i,"R"])) + abs(G- int(colours_df.loc[i,"G"]))+ abs(B- int(colours_df.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = colours_df.loc[i,"colour_name"]
    return cname

## MOUSE CLICK FUNCTION
## DOUBLE CLICK TO FIND COLOUR
def mouse_click(event, x, y, flags, param):
    # if double click on picture
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        # Access Pixel Values
        b,g,r = test_img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

## CREATE WINDOW AND ADD MOUSE CLICK FUNCTION
cv2.namedWindow('Colour Recognizer')
cv2.setMouseCallback('Colour Recognizer', mouse_click)

running = 1

while(running):
    cv2.imshow("Colour Recognizer",test_img)
    if (clicked):
        ## CREATING BLOCK THAT WILL DISPLAY TEXT CONTAINING COLOUR NAME AND RGB VALUES RESPECTIVELY
        cv2.rectangle(test_img,(20,20), (750,60), (0,0,0), -1)
        text = recognize_colour(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        cv2.putText(test_img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
            
        clicked=False

    #Exit when pressed 'esc' key    
    if (cv2.waitKey(100) & 0xFF) == 27:
        break

cv2.destroyAllWindows()
