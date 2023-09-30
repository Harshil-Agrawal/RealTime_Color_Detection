import cv2
import pandas as pd
import time

# Can take a video file as input or video stream from the webcam
cap = cv2.VideoCapture("C:/Users/harsh/Downloads/video (1080p).mp4")
#cap = cv2.VideoCapture(0)

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("C:/Users/harsh/Downloads/colors.csv", names=index, header=None)
r = g = b = x_pos = y_pos = 0


# Function to get the Color name from the dataset for which the RGB value is the closest.
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# Function to get x,y coordinates of mouse double click which will also give the RGB values 
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Outer Loop To keep the Video Stream on
while True:

    ret, frame = cap.read()
    clicked = False
    cv2.namedWindow('Video')
    # draw_function will be called when the mouse event occured
    cv2.setMouseCallback('Video', draw_function)
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)


    # Inner Loop will be executed when key(p) is clicked which will pause the video stream to a single frame 
    # This loop is used for the main task which is Color detection 
    if cv2.waitKey(1) == ord("p"):
        while True:
         
            cv2.imshow('Video', frame)
            
            # Display the color name once draw function is called and clicked is true
            if clicked:

                # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
                cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)

                # Creating text string to display( Color name and RGB values )
                text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

                # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
                cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                # For very light colours we will display text in black colour
                if r + g + b >= 600:
                    cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

                clicked = False


            # Key to get out of the loops
            # Key(p) to resume the video stream and Key(esc) to get out of both the loops and end the execution    
            key = cv2.waitKey(1)

            if key == ord("p"):
                break
            if key == 27:
                break
 
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
