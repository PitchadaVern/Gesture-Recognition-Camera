# Gesture-Recognition-Camera
Gesture-Controlled Camera using MediaPipe and OpenCV
This is a personal project using MediaPipe and OpenCV to control a camera using hand gestures. The goal is to take a photo from a distance, by using only hand gesture

# Overview
This project uses:
1. MediaPipe for gesture recognition
2. OpenCV for real-time camera and image display
3. Python for the entire implementation

# How It Works
1. Detect the hand using MediaPipe's hand landmark model
2. Track 21 hand keypoints, like fingertips and knuckles
3. Compare the gesture to known data
4. Recognize the gesture (if confidence > 50%)
5. Run commands based on the gesture
6. Show results using OpenCV in real-time

*Note: The phone shown in the demo is only used to record video. It is not part of the program.

# Gesture Commands
1. 👊 → countdown for 5 seconds, then Take photo
2. ✌️ → zoom in
3. ☝️ → zoom out
4. 👍 → change to greyscale
5. 👎 → change back to RGB

# for more information and demonstration
https://www.canva.com/design/DAF2LaebTo8/JdE-FAakOWK9Ln8UWRJUyA/view?utm_content=DAF2LaebTo8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hc5b7bf1da1

