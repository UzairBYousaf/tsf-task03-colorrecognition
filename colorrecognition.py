#importing dependancies to create an environment
import cv2
import pandas as pd

#loading both test image and csv file containing color data
img_path = 'sample-image.jpg'
csv_path = 'colors.csv'

#creating dataframe for color label
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

#reading image
img = cv2.imread(img_path)
img = cv2.resize(img, (1280,720))

#setting status as false unless clicked by Left Mouse Button
clicked = False

#getting R, G & B data from mouse cursor position on X-Y Plane
r = g = b = xpos = ypos = 0

#Defining function to get color name
def get_color_name(R,G,B):
	minimum = 1000 # minimum threshold of intensity
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B'])) # getting intensity value from image
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name'] # getting color name if intensity is less than threshold
	return cname

# Function to draw mouse cursor for easy navigation
def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

# Function to display color name
while True:
	cv2.imshow('image', img)
	if clicked:
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)
		text = get_color_name(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)
	if cv2.waitKey(20) & 0xFF == 27:
		break
cv2.destroyAllWindows()
