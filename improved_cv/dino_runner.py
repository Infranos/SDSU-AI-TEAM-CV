
#Author: Alexander Kirk, SDSU AI Club

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

import cv2
import time

from custom_ocr import create_ocr_template
from custom_ocr import determine_score

from motion_detector import grab_still_background
from motion_detector import retrieve_contourArea


def runner():
	try:

		#Launching Chrome's Dino-game through Selenium..
		driver = webdriver.Chrome()
		driver.get("chrome://network-error/-106")

		#Establish the automated jump key and begin the game
		jump = ActionChains(driver) 
		jump.send_keys(Keys.SPACE)
		jump.perform()

		#Ensure everything's loaded; pre-set variables
		time.sleep(1)
		score = 0
		old_score = 0
		high_score = 0
		timer_can_start = True
		default_increment = 0
		increment = default_increment

		#Our beautiful custom OCR templates
		digit_templates = create_ocr_template('offline-sprite-2x.png')

		#Capture our screen through Selenium and grab the ROIs for obstacle dodging
		screenshot = "game_screenshot.png"
		driver.save_screenshot(screenshot)
		first_frame = grab_still_background(screenshot, True)

		#Now as long as we don't crash..: 
		while score <  700:
			driver.save_screenshot(screenshot)
			
			#Our custom OCR for score detection:
			score = determine_score(screenshot, digit_templates)

			#If we have started over, truly, and do not get a false positive from a flashing score,
			#then reset the increment
			if 0 < score < 12:
				increment = default_increment

			
			#Every 100 points, we slightly increment the ROI to the right
			if (score < 601):
				if (increment - default_increment) < int(score / 100):
					increment = int(score / 100) + default_increment
					print("New increment: {}".format(increment))

			#Motion detection for object dodging
			contour_area = retrieve_contourArea(screenshot, first_frame, increment, True)
			if contour_area > 25:
				jump.perform()
				

			print("Score: {}".format(score))


			#Basically, if the score is the same for multiple passes, run a timer:
			if old_score == score:
				if timer_can_start:
					start = time.time()
					timer_can_start = False
				else:
					#If the time passed exceeds two seconds, we've crashed our dino
					elapsed = time.time() - start
					if elapsed > 2:
						if score > high_score:
							high_score = score
						timer_can_start = True
						jump.perform()
					print("Time Elapsed: {}".format(elapsed))
			else:
				old_score = score
				timer_can_start = True
				
		print("Score of 700 reached!  Closing..")
		driver.close()

	except WebDriverException:
		pass


runner()
