import os
import pickle
import numpy as np
import cvzone
import cv2  # for using webcam
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition2303-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition2303.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # capturing video #error might come in this step. If you are using laptop and have only one camera then set it to
                        # 0 otherwise 1 or 2.

cap.set(3, 640)  # as I am using graphics this two line is for graphics window
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

#Importing the mode images into a list.
folderModePath = 'Resources/Modes' #initializing modes as list.
modePathList = os.listdir(folderModePath) #mode path list.
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))



#Load the encoding file
print ("Loading encoded file")
file = open("EncodeFile.p", 'rb')
encodeListknownWithIDs = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListknownWithIDs
print("Encoded file loaded")
#print(studentIds)

modeType = 0
counter = 0
id = 0
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType] #imgModeList for showing the images. If I put 1 then it will show the first stage otherwise 0 for initial stage.

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
       matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
       faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
      # print("matches", matches)
      # print("Facedis", faceDis)

       matchIndex = np.argmin(faceDis)
      # print("Match Index", matchIndex)

       if matches[matchIndex]:
           # print("Known Face Detected")
           # print(studentIds[matchIndex])
           y1,x2,y2,x1 = faceLoc
           y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
           bbox = 55+x1, 162+y1, x2-x1, y2-y1
           imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
           id = studentIds[matchIndex]

           if counter ==0:
            counter = 1
            modeType = 1
    if counter!=0:
        if counter ==1:
            #getting the data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            #getting the image from storage
            #blob = bucket.get_blob(f'images/{id}.jpg')
           # blob = bucket.get_blob(f'images/{id}.jpeg')
           # array = np.frombuffer(blob.download_as_string(), np.uint8)
            #imgStudent = cv2.imdecode(array, cv2.COLOR_BGR2RGB)
        cv2.putText(imgBackground, str(studentInfo['Total_attendance']), (861,125),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)

        (w,h), _ = cv2.getTextSize(studentInfo['Name'],  cv2.FONT_HERSHEY_COMPLEX, 0.9,1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(studentInfo['Name']), (808+offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 1)
        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentInfo['Standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentInfo['last_attendance_time']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 0, 0), 1)

        #imgBackground[175:175+216, 909:909+216] = imgStudent
        counter +=1
   # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)