from PIL import Image

import cv2

#Your code should:
#	A: Extract the roi (region of interest)
#	B: Apply pre-processing
#	C: Apply contour detection
#	D: If a new object is detected, return true
#
#	Don't worry, it seems like a large task, but you got dis. 
#	Follow the comments, ask questions, and read the example object detection if you get stuck!

def grab_still_background(screenshot_img):

	#We'll start easy.  All you have to do for this function is alter the crop and pre-process lines

	screenshot = Image.open(screenshot_img)
	w = screenshot.size[0]
	h = screenshot.size[1]
	#Edit below line:
	#You'll want to grab a small box area just right of our t-rex, instead of the whole thing
	#To get a decent still background-image, avoid capturing the ground
	################################################################################################
	background = screenshot.crop((295, 120, 390, 162))
	################################################################################################
	background.save("first_frame.png")
	
	
	first_frame = cv2.imread("first_frame.png")
	#Edit below line:
	#Apply basic pre-processing by converting the image to gray-scale
	################################################################################################
	first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
	################################################################################################
	return first_frame
	
#=======================================================================================================

def should_jump(screenshot_img, first_frame, verbose = False):

	#Grabs the area just after T-rex
	screenshot = Image.open(screenshot_img)
	w = screenshot.size[0]
	h = screenshot.size[1]
	#Edit below line:
	#Same as the still background's set
	################################################################################################
	roi = screenshot.crop((295, 120, 390, 162)) 
	################################################################################################
	roi.save("current_frame.png")


	#With the ROI saved, we'll need to re-read the image in cv2 and apply pre-processing:
	current_frame = cv2.imread("current_frame.png")
	current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

	
	#We'll need to get the difference between the first frame and the current frame:
	#Then, we'll need to pre-process the difference:
	difference = cv2.absdiff(first_frame, current_frame)
	processed_img = cv2.threshold(difference, 0, 255, cv2.THRESH_BINARY)[1]
 
	# Dilation fills in basic holes.  We then apply contours
	processed_img = cv2.dilate(processed_img, None, iterations=2)
	_, contours, _ = cv2.findContours(processed_img.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	#Good news, nothing to edit here :D
	for contour in contours:
		if verbose:
			print("Con: {}".format(cv2.contourArea(contour)))
		
		#Helps us ignore false positives and weak matches
		if cv2.contourArea(contour) < 25:
			continue 

		if verbose:
			print("should jump")

		return True

	return False
