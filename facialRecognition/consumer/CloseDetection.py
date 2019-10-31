def CloseDetection(frame,detector,predictor,type="mouth"):
    # import the necessary packages
    from scipy.spatial import distance as dist
    from imutils import face_utils
    import cv2
    
    def mouth_aspect_ratio(mouth):
        # compute the euclidean distance between the vertical
        #       51  52  53 
        #   49                55
        #       59  58  57
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[3], mouth[9])
        C = dist.euclidean(mouth[4], mouth[8])

    	# compute the euclidean distance between the horizontal
        D = dist.euclidean(mouth[0], mouth[6])
        # compute the eye aspect ratio
        ear = (A + B + C) / (3.0 * D)
    
        # return the eye aspect ratio
        return ear


    def eye_aspect_ratio(eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

    	# compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear
 
    AR_THRESH = 0.5

    # initialize the frame counters and the total number of blinks
    count = 0    
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    # loop over the face detections
    ear = 0
    for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        if type == "eye":
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
        elif type == "mouth":
            mouth = shape[mStart:mEnd]
            ear = mouth_aspect_ratio(mouth)
        else:
            print("no facial object type is defined")
        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
#        leftEyeHull = cv2.convexHull(leftEye)
#        rightEyeHull = cv2.convexHull(rightEye)
#        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
#        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
        if ear > AR_THRESH:
            count = 1
#        print("ear: %.2f"%ear)
    return count,ear

if __name__ =='__main__':
    import cv2
    import dlib
    
    webcam = cv2.VideoCapture(0)
    shape_predictor="shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)       
    c = 0
    f = 0
    while f < 20:
        _,frame = webcam.read()
        f += 1
        count,ear = CloseDetection(frame,detector,predictor,"mouth")
        c += ear
        cv2.imshow("Frame",frame)
        cv2.waitKey(50)
#    c = c/f
#    print(str(count),"ear: %.2f"%c)
    webcam.release()
    cv2.destroyAllWindows()