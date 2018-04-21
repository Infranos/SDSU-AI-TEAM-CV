HI!  Welcome to the 2018 AI Team CV workshop.
This code runs Google's Dinosaur game, tracks the score, and looks ahead to dodge incoming objects.
The purpose of this code is to help teach the basics of computer vision, and is not yet supposed to play the game fully.

In here, you'll find:
-dino_runner.py
	Our main program

-custom_ocr.py
	For our demo; tracks the score

-motion_detector.py
	The code we have to edit.
	Tracks approaching obstacles
	
-motion_detector_complete.py
	Cheatsheet for the above.
	So we know what the goal looks like

-steps_taken.txt
	Just a quick overview of our methodology/reasoning
	

Update:  In the improvedcv directory, you'll find changes I've made since our workshop.  I've added things like a sliding ROI (shifts the region of interest as the score/speed increases) and a proper selenium exit.  I also return the pure contour area score instead of a boolean T/F should_jump, so you can better assign both a ground truth and a supposed_choice for your own neural network implementation.

Of course, if you simply don't want any of my modifications and want the pure workshop's code to tweak on your own, give it a shot.  Neither the base or improved version is perfect anyway, and are ready for your own tweaks.  I'm excited to see what you guys will do with this.

If you do something you're proud of, be sure to both give a shoutout in your work to SDSU AI Club, and of course to let us know at sdsuaiclub@gmail.com, so we can give a shout out to you as well :)

Cheers, and happy coding!
