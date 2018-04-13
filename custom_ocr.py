from PIL import Image

import cv2
from imutils import contours
import imutils
import numpy as np

from pytesseract import image_to_string

# Author: Alexander Kirk
# Motive: To demonstrate custom OCR for SDSU AI Club
# Objective: Teach program to better recognize score, as PyTesseract was not up to standard

# Reference: Adrian Rosebrock
# https://www.pyimagesearch.com/2017/07/17/credit-card-ocr-with-opencv-and-python/

#=======================================================================================================
#Grab Sprite Sheet and Extract only the Digit Template

def create_ocr_template(sprite_sheet_img = "offline-sprite-2x.png", verbose = False):

	#Grabs just the digits and "HI"
	sprite_sheet = Image.open(sprite_sheet_img)
	w = sprite_sheet.size[0]
	h = sprite_sheet.size[1]
	digit_set = sprite_sheet.crop((950, 0, w - 1210, h - 105))
	digit_set.save("digit_set.png")

#=======================================================================================================
#Have Program Read the Digit Template

	#Grab digit set and pre-process to make it easier for computer to read
	digit_set = cv2.imread("digit_set.png")
	digit_set = cv2.cvtColor(digit_set, cv2.COLOR_BGR2GRAY) #Gray digits become white on black
	digit_set = cv2.threshold(digit_set, 0, 255, cv2.THRESH_OTSU)[1] #Image gets less noise
	if verbose:
		cv2.imwrite("processed_image.png", digit_set)

	#Use newly pre-processed image to identify digits' boundaries via contours
	our_contours = cv2.findContours(digit_set.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	our_contours = our_contours[0] if imutils.is_cv2() else our_contours[1]
	our_contours = contours.sort_contours(our_contours, method="left-to-right")[0]
	digit_templates = {}

	#Use contours to grab the whole digits
	counter = 0 #Used for file naming when verbose
	for (current_index, contour_index) in enumerate(our_contours):
		(x, y, w, h) = cv2.boundingRect(contour_index)
		roi = digit_set[y:y + h, x:x + w] #region of interest
		roi = cv2.resize(roi, (5, 7)) 
		digit_templates[current_index] = roi
		if verbose:
			template_digit_file = "template_digit{}.png".format(counter)
			cv2.imwrite(template_digit_file, roi)
		counter += 1

	#Contains our digit templates
	return digit_templates

#=======================================================================================================
#Identify Digits in our Actual Image:

def determine_score(screenshot, digit_templates, verbose = False):

	#Crop score image from our overall screenshot:
	overall_img = Image.open(screenshot)
	w = overall_img.size[0]
	h = overall_img.size[1]
	dino_score_img = overall_img.crop((w - 300, 30, w - 220, h - 520))
	dino_score_img.save("score_img.png")

	#Pre-process our score image to be properly read in OpenCV
	dino_score = cv2.imread("score_img.png") #Must be read through cv2 to apply thresholding
	dino_score = cv2.cvtColor(dino_score, cv2.COLOR_BGR2GRAY)
	dino_score = cv2.threshold(dino_score, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]	
	if verbose:
		cv2.imwrite("processed_score.png", dino_score)

	#Apply contours to identify digit boundaries to our image
	digit_contours = cv2.findContours(dino_score.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	digit_contours = digit_contours[0] if imutils.is_cv2() else digit_contours[1]
	try:
		digit_contours = contours.sort_contours(digit_contours,
			method="left-to-right")[0]
	except:
		print("Flashing Score")
		return 0

	# Loop over the digit contours to ID digits, resizing them to our templates
	output = [] #This will be the result of our hard-work
	counter = 0 #Just a visual aid for verbosity/debugging
	for contour in digit_contours:
		(x, y, w, h) = cv2.boundingRect(contour)
		roi = dino_score[y:y + h, x:x + w]
		roi = cv2.resize(roi, (5, 7))
		if verbose:
			score_digit_file = "score_digit{}.png".format(counter)
			cv2.imwrite(score_digit_name, roi)
		counter += 1

		#Create a scoring system to determine how closely a template matches
		scores = []

		#Test how closely a template digit matches with a digit in our image
		for (digit, digitROI) in digit_templates.items():
			result = cv2.matchTemplate(roi, digitROI,
				cv2.TM_CCOEFF)
			(_, score, _, _) = cv2.minMaxLoc(result)
			scores.append(score)

		#The highest scored template match is the one we'll use for our digit
		output.append(str(np.argmax(scores)))
	 
	#Prepare our result
	custom_result = ''.join(output)
	if verbose:
		print("Custom OCR Result: {}".format(custom_result))

	try:
		returning_score = int(custom_result.lstrip())
	except ValueError:
		returning_score = 0

#=======================================================================================================
#Laugh as PyTesseract's Method Fails:

	if verbose:
		tesser_result = image_to_string(Image.open(dino_score_img))
		print("Tesseract result: {}".format(tesser_result))

#=======================================================================================================
#Finish:
	
	return returning_score
