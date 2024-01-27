import cv2
import pandas as pd

# read values from csv file
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# funtion to get the closest color name
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname



cap = cv2.VideoCapture(0)
while(1):
    _, frame = cap.read()
    height, width, _ = frame.shape

    # calculate centre position
    cx = int(width / 2)
    cy = int(height / 2)

    # Flip the frame horizontally (mirror effect)
    frame = cv2.flip(frame, 1)


    pixel_center = frame[cy, cx]

    B, G, R = pixel_center

    #get color name
    color_name = get_color_name(R,G,B)


    # Create a black box
    cv2.rectangle(frame, (10, 10), (200, 50), (0, 0, 0), -1)
    cv2.circle(frame ,(220,30),20, (int (B),int (G), int (R)),-1 )

    # Display the color name in white on the black box
    cv2.putText(frame, color_name, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    #to print corresponding B G R values
    print(pixel_center)

    cv2.circle(frame,(cx,cy),3,(225, 225, 225), -1)

    #display image/video
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
