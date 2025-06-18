import cv2
import mediapipe as mp
import time
import numpy as np 
import winsound

properties=["CV_CAP_PROP_FRAME_WIDTH",# Width of the frames in the video stream.
            "CV_CAP_PROP_FRAME_HEIGHT",# Height of the frames in the video stream.
            "CV_CAP_PROP_BRIGHTNESS",# Brightness of the image (only for cameras).
            "CV_CAP_PROP_CONTRAST",# Contrast of the image (only for cameras).
            "CV_CAP_PROP_SATURATION",# Saturation of the image (only for cameras).
            "CV_CAP_PROP_GAIN",# Gain of the image (only for cameras).
            "CV_CAP_PROP_EXPOSURE"]


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

video = cv2.VideoCapture(0)

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global zoom_factor  # Declare zoom_factor as a global variable
    global frame, blink_start_time, prev, TIMER
    global ad, k
    if result.gestures != []:
        print(result.gestures[0][0].category_name)
        
        #capture
        if result.gestures[0][0].category_name == "Closed_Fist":
            prev = time.time()
            TIMER = 5

        #zoom in/ zoom out
        if result.gestures[0][0].category_name == "Victory":
            zoom_factor += 0.01
        
        if result.gestures[0][0].category_name == "Pointing_Up":
            zoom_factor -= 0.01
            if zoom_factor < 0.1:  # Ensure zoom factor does not go below 0.1
                zoom_factor = 0.1
        
        if result.gestures[0][0].category_name == "Thumb_Up":
            ad = True
            k = 0
        
        if result.gestures[0][0].category_name == "Thumb_Down":
            ad = False

                 
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
zoom_factor = 1.0
is_blink_frame = False
blink_duration = 0.5  # Set blink duration in seconds
blink_start_time = 0
prev = 0
TIMER = 5 
change_to_grey = False
ad = False
k=0
frequency = 2000
duration = 1000


with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)

        # Resize the frame based on the zoom factor
        resized_frame = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)

        #countdown
        c_time = time.time() - prev
        if 0 <= c_time <= TIMER:
            while TIMER >= 0:
                ret, frame = video.read()
                if ad:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
                numframe = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)
                font = cv2.FONT_HERSHEY_SIMPLEX 
                cv2.putText(numframe, str(TIMER),  
                                    (200, 250), font, 
                                    7, (0, 0, 255), 
                                    8, cv2.LINE_AA)
                cv2.imshow("Hand Recognition", numframe)
                cv2.waitKey(125)
                #winsound.Beep(frequency, duration) #in progress
  
            # current time 
                cur = time.time() 
  
            # Update and keep track of Countdown 
            # if time elapsed is one second  
            # then decrease the counter 
                if cur-prev >= 1: 
                    prev = cur 
                    TIMER = TIMER-1
  
            else: 
                ret, frame = video.read()
                resized_frame = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)
                if ad:
                    resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
                    k=1
                    ad=False 
            # Display the clicked frame for 2  
            # sec.You can increase time in  
            # waitKey also 
                cv2.imshow("Hand Recognition", resized_frame)
  
            # Save the frame 
                cv2.imwrite('shutter.png', resized_frame)
                blink_start_time = time.time()  # Start time for blink effect


        # Blink effect
        elapsed_time = time.time() - blink_start_time
        if 0 <= elapsed_time <= blink_duration:
            alpha = 1.0 - elapsed_time / blink_duration
            is_blink_frame = True
            resized_frame = cv2.addWeighted(resized_frame, alpha, resized_frame, 0, 0)


    
        # Display the frame for the blink effect
        if is_blink_frame:
            cv2.imshow("Hand Recognition", resized_frame)
        else:
        # Display the frame without blink effect
            cv2.imshow("Hand Recognition", resized_frame)
        
        #change to gray scale
        intitial = resized_frame
        if ad:
            if k != 1:
                intitial = resized_frame
                resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY) 
            cv2.imshow("Hand Recognition", resized_frame)
        else:
            resized_frame = intitial
            k=0
            cv2.imshow("Hand Recognition", resized_frame)

  

        if cv2.waitKey(5) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()

## Read logo and resize 
            #logo = cv2.imread('great.gif') 
            #size = 300
            #logo = cv2.resize(logo, (size, size)) 
  
            # Create a mask of logo 
            #img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) 
            #ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
 # Region of Image (ROI), where we want to insert logo 
            #roi = resized_frame[-size-100:-100, -size-250:-250] 
  
            # Set an index of where the mask is 
            #roi[np.where(mask)] = 0
            #roi += logo