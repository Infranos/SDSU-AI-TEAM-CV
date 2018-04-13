
#Author: Alexander Kirk, SDSU AI Club

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import cv2
import time

from custom_ocr import create_ocr_template
from custom_ocr import determine_score

from motion_detector import grab_still_background
from motion_detector import should_jump


def runner():

	#Launching Chrome's Dino-game through Selenium..
	driver = webdriver.Chrome()
	driver.get("chrome://network-error/-106")

	#Establish the automated jump key and begin the game
	actions = ActionChains(driver)
	actions.send_keys(Keys.SPACE)
	actions.perform()

	#Ensure everything's loaded; pre-set variables
	time.sleep(1)
	marathon_end = False
	old_score = 0
	timer_can_start = True
	high_score = 0

	#Our beautiful custom OCR templates
	digit_templates = create_ocr_template('offline-sprite-2x.png')

	#Capture our screen through Selenium and grab the ROI for obstacle dodging
	screenshot = "game_screenshot.png"
	driver.save_screenshot(screenshot)
	first_frame = grab_still_background(screenshot)

	#Now as long as we don't crash..: 
	while not marathon_end:
		driver.save_screenshot(screenshot)
		
		#Our custom OCR for score detection.  Dw, I'll demo this:
		score = determine_score(screenshot, digit_templates)

		#Motion detection for object dodging.  Yeah sorry, you're editing the function code ;)
		jump = should_jump(screenshot, first_frame)
		if jump:
			actions.perform()
			

		print(score)

		#Basically, if the score is the same for multiple passes, run a timer:
		if old_score == score:
			if timer_can_start:
				start = time.time()
				timer_can_start = False
			else:
				#If the time passed exceeds two seconds, we've crashed our dino
				elapsed = time.time() - start
				if elapsed > 2:
					marathon_end = True #Commenting this out will allow the marathon to continue
					if score > high_score:
						high_score = score
					timer_can_start = True
					actions.perform()
				print(elapsed)
		else:
			old_score = score
			timer_can_start = True
			
	driver.close()


runner()
