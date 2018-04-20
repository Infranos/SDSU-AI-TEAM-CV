from PIL import Image

import cv2

#=======================================================================================================
#This function makes its return from our previous Computer Vision workshop.
#It grabs the region to the right of our dinosaur (dodging the ground itself),
#and uses it to later see if an object enters the space.

#A new value, increment, was also added.
#Increment basically helps our program see approaching obstacles by slightly 
#adjusting the ROI as the score/speed increases.

def grab_still_background(screenshot_img, increment = 0, verbose = False):

	screenshot = Image.open(screenshot_img)
	w = screenshot.size[0]
	h = screenshot.size[1]

	start_w = int(w * 0.3722) + int(increment * 0.01 * w) 
	start_h = int(h * 0.2064)
	end_w = int(w * 0.4625) + int(increment * 0.01 * w) 
	end_h = int(h * 0.2718)
	background = screenshot.crop((start_w, start_h, end_w, end_h))
	background.save("first_frame.png")

	#Draws a rectangle around our ROI
	if verbose:
		background = cv2.imread(screenshot_img)
		screenshot_with_roi = cv2.rectangle(background, (start_w, start_h), (end_w, end_h), (0,255,0),3)
		cv2.imwrite("screenshot_with_roi.png", screenshot_with_roi)
	
	first_frame = cv2.imread("first_frame.png")
	first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
	return first_frame
	
#=======================================================================================================

def should_jump(screenshot_img, first_frame, increment = 0, verbose = False):

	object_present = False

	#Grabs the area just after T-rex
	screenshot = Image.open(screenshot_img)
	w = screenshot.size[0]
	h = screenshot.size[1]
	
	start_w = int(w * 0.3722) + int(increment * 0.01 * w)
	start_h = int(h * 0.2064)
	end_w = int(w * 0.4625) + int(increment * 0.01 * w) 
	end_h = int(h * 0.2718)
	roi = screenshot.crop((start_w, start_h, end_w, end_h))
	roi.save("current_frame.png")

	if verbose:
		background = cv2.imread(screenshot_img)
		screenshot_with_roi = cv2.rectangle(background, (start_w, start_h), 
			(end_w, end_h), (0,255,0),3)
		cv2.imwrite("screenshot_with_roi.png", screenshot_with_roi)

	#With the ROI saved, we re-read the image in cv2 and apply pre-processing:
	current_frame = cv2.imread("current_frame.png")
	current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
	
	#We'll get the difference between the first frame and the current frame:
	#Then, we pre-process the difference:
	difference = cv2.absdiff(first_frame, current_frame)
	processed_img = cv2.threshold(difference, 0, 255, cv2.THRESH_BINARY)[1]
 
	#Dilation fills in basic holes.  We then apply contours
	processed_img = cv2.dilate(processed_img, None, iterations=2)
	_, contours, _ = cv2.findContours(processed_img.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	#Determines whether or not an object is present:
	for contour in contours:
		if verbose:
			print("Con: {}".format(cv2.contourArea(contour)))
		
		#Helps us ignore false positives and weak matches
		if cv2.contourArea(contour) < 25:
			object_present = False
		else:
			object_present = True

	return object_present
