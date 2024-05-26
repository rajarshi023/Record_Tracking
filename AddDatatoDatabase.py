import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition2303-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    "123456" :
        {
            "Name" : "Rajarshi Bhattacharya",
            "major" : "8",
            "Starting_Year" : "1.1.21",
            "Total_attendance" : 6,
            "Standing" : "G",
            "Year" : "6/12",
            "last_attendance_time" : "2022-12-11 00:54:34"
        },
    "234567" :
        {
            "Name" : "Leonel Messi",
            "major" : "Football",
            "Starting Year" : 2000,
            "Total_attendance" : 6,
            "Standing" : "E",
            "Year" : 3/10,
            "last_attendance_time" : "2022-12-11 00:54:34"
        },
    "3456789" :
        {
            "Name" : "Elon Musk",
            "major" : "Tesla",
            "Starting Year" : 2018,
            "Total_attendance" : 6,
            "Standing" : "A",
            "Year" : 5/12,
            "last_attendance_time" : "2022-12-11 00:54:34"
        },
    "4567891" :
        {
            "Name" : "Cristiano Ronaldo",
            "major" : "Football",
            "Starting Year" : 2000,
            "Total_attendance" : 6,
            "Standing" : "E",
            "Year" : 8/12,
            "last_attendance_time" : "2022-12-11 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)