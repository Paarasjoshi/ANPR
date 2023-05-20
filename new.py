from tkinter import *
from twilio.rest import Client
sid="ACf026f2aef2b48ac3ad977e517d826ea4"
auttoken="76f27b562a5a1d835ffcb9bd4b620665"

import requests  # library for connecting fast2sms server and python
import json  # library for pretty representation of dictionary
import easyocr

def window(v_no,state):
    root = Tk()
    root.geometry("500x250")
    root.title("Mayank")
    Label(root, text="Details").pack()
    Label(root,text=v_no).pack()
    Label(root,text=f"Vehicle Registration Area is {state} ").pack()
    Button(root, text="Submit").pack()
    root.mainloop()





message=f"UK04AG5095 Your vehicle spotted at wrong parking location XYZ,As Per motor vehicle Act 2002 You have beign fined for this Rs.500 submit fine at RTO office" \
        f"or can pay online through the given link fine Uid UK04AG509501 ignore if already paid"

#
dict={"AP":"Andhra Pradesh","AR": "Arunachal Pradesh","AS":"ASSAM","BR":"BIHAR","CG":"Chhattisgarh","GA":"GOA",
      "GJ":"GUJRAT","HR":"HARYANA","HP":"Himanchal Prdaesh","JH":"Jharkhand","KA":"Karnataka","KL":"Kerela","MP":"Madhya Pradesh","DL":"Delhi",
"AN":"Andaman and Nicobar Islands", "CH":"Chandigarh", "DN":"Dadra and Nagar Haveli" ,"DD":"Daman and Diu","JK":"Jammu and Kashmir" ,"LA":"Ladakh" ,
      "LD":"Lakshadweep", "PY":"Puducherry",
"MP":"Madhya Pradesh" ,"MH":"Maharashtra" ,"MN":"Manipur", "ML":"Meghalaya" ,"MZ":"Mizoram", "NL":"Nagaland" ,"OD":"Odisha" ,"PB":"Punjab", "RJ":"Rajasthan" ,
      "SK":"Sikkim", "TN":"Tamil Nadu" ,"TS":"Telangana", "TR":"Tripura", "UP":"Uttar Pradesh" ,"UK":"Uttarakhand", "WB":"West Bengal"
#
      }

import cv2
import easyocr
harcascade = "C:\\Users\\soumy\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
            img_roi = img[y: y + h, x:x + w]
            cv2.imshow("Number Plate", img_roi)

    cv2.imshow("INPUT FEED", img)


    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scanned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("INPUT FEED", img)
        cv2.waitKey(500)

        reder=easyocr.Reader(['en'])
        result=reder.readtext("plates/scanned_img_" + str(count) + ".jpg")
        n_plate = result[0][1]
        stae = n_plate[:2]


        try:
            print(f"Vehicle Number {n_plate}")
            print(f"Vehicle Registration area is {dict[stae]}")
            print(f"Owner Name xxxxxx")

            count += 1

            window(n_plate,stae)
            cl = Client(sid, auttoken)
            cl.messages.create(body=message, from_='+12525126957', to='+917017482038')
        except Exception as e:
            print("NOT ABLE TO READ IT PROPERLY")