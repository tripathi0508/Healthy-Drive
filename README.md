# GestureKeyboardControl
An openCV project in python to control WASD keys through hand gestures based on color detection techniques.
The colorDetection.py program could be used to calibrate the color used as glove and the HSV values are to be filled in the yellowUpper and yellowLower variables in MainControl.py file.
The mainControl.py file makes use of color detection to make contours from mask and two circles are formed at the center of the contours.
These circles are tracked and teh window is divided into three parts (upper, lower, centre) horizontally and two parts vertically(left, right).
The keys are pressed using DirectKeys.py file which is derived from https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game.
W,S keys are in the right part of the screen and A,D in the left part.
*For better gameplay, the webcam frame could be flipped using flip function.
