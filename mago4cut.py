from tkinter import *
from PIL import Image

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import tkinter as tk
import tkinter.font
import RPi.GPIO as GPIO
import cv2
import numpy as np
import smtplib

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
root = Tk()  # create root window
root.title("Basic GUI Layout")
root.geometry("1920x1080")# title of the GUI window
root.maxsize(2000, 2000)  # specify the max size the window can expand to
root.config(bg="white")  # specify background color
#global
global backPath
global cnt
global capFlag
global btnFlag
global capPath
global resultPath
global l_h
global l_s
global l_v
global u_h
global u_s
global u_v

btnFlag = True
capFlag = True

resultPath = ["/home/pi/Desktop/Img/result1.png", "/home/pi/Desktop/Img/result2.png", "/home/pi/Desktop/Img/result3.png", "/home/pi/Desktop/Img/result4.png"]

cnt = 0

l_h = 0
u_h = 180
l_s = 170
u_s = 255
l_v = 100
u_v = 255

back_frame = tk.Frame(root, width=1920, height=900, bg="white")
back_frame.pack()

left_frame = tk.Frame(back_frame, bg='white', borderwidth=2, relief="solid")
left_frame.pack(side="left", padx=10, pady=10)
right_frame = tk.Frame(back_frame, bg='white')
right_frame.pack(side="right", padx=10, pady=10)

font = tkinter.font.Font(family="맑은 고딕", size=20)

#750x450
imgs = [0 for i in range(4)]

global imgLabels

imgLabels = [0 for i in range(4)]

index = [[0, 0], [0, 1], [1, 0], [1, 1]]

for i in range(len(imgs)):

    imgs[i] = tk.PhotoImage(file="/home/pi/Desktop/Img/back" + "1,2,3,4".split(",")[i] + ".png")
    imgLabels[i] = tk.Label(right_frame, bg="black",image=imgs[i])
    imgLabels[i].grid(row=index[i][0], column=index[i][1], padx=10, pady=10)

Label(left_frame, text="MAGO 4 CUT", background="white", fg="black", font=font, borderwidth=1, relief="solid").grid(row=0, column=0, ipadx=73)
#250x250
logoImg = tk.PhotoImage(file="/home/pi/Desktop/Img/image/logo.png")
logo = tk.Label(left_frame, bg="white", image=logoImg, borderwidth=1, relief="solid")
logo.grid(row=1, column=0, ipadx=33)

tool_bar = tk.Frame(left_frame, bg="white", borderwidth=1, relief="solid", width=100)
tool_bar.grid(row=2, column=0)

group = IntVar()

rbtns = [0 for i in range(5)]

def imageEvent1():
    global btnFlag
    if btnFlag == True:
        btnFlag = False
        global backPath
        backPath = "/home/pi/Desktop/Img/back1.png"
        cap()
        chromakey()
def imageEvent2():
    global btnFlag
    if btnFlag == True:
        btnFlag = False
        global backPath
        backPath = "/home/pi/Desktop/Img/back2.png"
        cap()
        chromakey()
    if btnFlag == True:
        btnFlag = False
        global backPath
        backPath = "/home/pi/Desktop/Img/back3.png"
        cap()
        chromakey()
def imageEvent4():
    global btnFlag

    if btnFlag == True:
        btnFlag = False
        global backPath
        backPath = "/home/pi/Desktop/Img/back4.png"
        cap()
        chromakey()

def cap():

    global cnt
    global imgLabels
    global capPath
    global backPath
    global resultPath
    global capFlag
    global l_h
    global l_s
    global l_v
    global u_h
    global u_s
    global u_v

    capFlag = True

    if(cnt > 3):
        cnt = 0

    capPath = "/home/pi/Desktop/Img/capPath.png"
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    flag = False
    flag2 = False

    def nothing(x):
        pass
    panel = np.zeros([100,400], np.uint8)

    while True:

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (750, 450))

        cv2.imwrite(capPath, frame)
        img = cv2.imread(capPath)
        window = cv2.imread(backPath)
        window = cv2.resize(window, (750, 450))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([l_h,l_s,l_v])
        upper = np.array([u_h,u_s,u_v])

        mask = cv2.inRange(hsv, lower, upper)
        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(img, img, mask=mask)
        fg = cv2.bitwise_and(img, img, mask=mask_inv)

        window_bg = cv2.bitwise_and(window, window, mask=mask)
        result = cv2.addWeighted(src1=fg, src2=window_bg, alpha=1, beta=1, gamma=0)

        cv2.imshow('result', result)

        imsi = (cv2.waitKey(30) & 0xFF)

        inputIO = GPIO.input(17)
        if imsi == ord('x'):
            if flag == True:
                flag = False
            else:
                flag = True

        if capFlag == False:
            cv2.imwrite(resultPath[cnt], frame)
            break
        if inputIO == 0:
            capFlag = False
        
        if imsi == ord('c'):
            capFlag = False
        if flag == True:
            if flag2 == False:
                cv2.namedWindow('panel')
                cv2.createTrackbar('L-H', 'panel', 0,179, nothing)
                cv2.createTrackbar('U-H', 'panel', 179,179, nothing)
                cv2.createTrackbar('L-S', 'panel', 0,255, nothing)
                cv2.createTrackbar('U-S', 'panel', 255,255, nothing)
                cv2.createTrackbar('L-V', 'panel', 0,255, nothing)
                cv2.createTrackbar('U-V', 'panel', 255,255, nothing)
                flag2 = True
            l_h = cv2.getTrackbarPos('L-H', 'panel')
            u_h = cv2.getTrackbarPos('U-H', 'panel')
            l_s = cv2.getTrackbarPos('L-S', 'panel')
            u_s = cv2.getTrackbarPos('U-S', 'panel')
            l_v = cv2.getTrackbarPos('L-V', 'panel')
            u_v = cv2.getTrackbarPos('U-V', 'panel')
            cv2.resize(panel, (750, 450))
            cv2.imshow('panel', panel)
    cap.release()
    cv2.destroyAllWindows()
def chromakey():
   
    global cnt
    global imgLabels
    global capPath
    global backPath
    global resultPath
    global l_h
    global l_s
    global l_v
    global u_h
    global u_s
    global u_v
    global btnFlag

    cap = cv2.imread(capPath)
    window = cv2.imread(backPath)
    window = cv2.resize(window, (cap.shape[1],cap.shape[0])) # width, height 고정 크기

    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    lower_green = np.array([l_h,l_s,l_v])
    upper_green = np.array([u_h,u_s,u_v])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask) # 마스크를 거꾸로만들어라

    bg = cv2.bitwise_and(cap, cap, mask=mask) # lg와 ug 사이 놈들을 마스크 사이놈들만 살린다
    fg = cv2.bitwise_and(cap, cap, mask=mask_inv) # 위에거의 반대

    window_bg = cv2.bitwise_and(window, window, mask=mask)

    result = cv2.addWeighted(src1 = fg, src2=window_bg, alpha=1, beta=1, gamma=0)

    cv2.imwrite(resultPath[cnt], result)

    resultPath[cnt] = resultPath[cnt]
    cv2.destroyAllWindows()
    imsiImage = tk.PhotoImage(file=resultPath[cnt])
    imgLabels[cnt].configure(image=imsiImage)
    imgLabels[cnt].image = imsiImage
    cnt+=1
    btnFlag = True
def reset():

    global cnt
    global imgLabels
    global txtbox
    cnt = 0
    for i in range(4):
        imsiImage = tk.PhotoImage(file="/home/pi/Desktop/Img/back" + "1,2,3,4".split(",")[i] + ".png")
        imgLabels[i].configure(image=imsiImage)
        imgLabels[i].image = imsiImage
    txtbox.delete("1.0", "end")
rbtns[0] = tk.Button(tool_bar, text="라벤더 색", bg="white", font=font, width = 11, height = 2, borderwidth=1, relief="solid", command = lambda: [imageEvent1(), cap(), chromakey()])
rbtns[0].grid(row=0, column=0, ipadx = 61)

rbtns[1] = tk.Button(tool_bar, text="미니언즈", bg="white", font=font, width = 11, height = 2, borderwidth=1, relief="solid", command = lambda: [imageEvent2(), cap(), chromakey()])
rbtns[1].grid(row=1, column=0, ipadx = 61)

rbtns[2] = tk.Button(tool_bar, text="짱구", bg="white", font=font, width = 11, height = 2, borderwidth=1, relief="solid", command = lambda: [imageEvent3(), cap(), chromakey()])
rbtns[2].grid(row=2, column=0, ipadx = 61)

rbtns[3] = tk.Button(tool_bar, text="우리학교", bg="white", font=font, width = 11, height = 2, borderwidth=1, relief="solid", command = lambda: [imageEvent4(), cap(), chromakey()])
rbtns[3].grid(row=3, column=0, ipadx = 61)

rbtns[4] = tk.Button(tool_bar, text="RESET", bg="white", font=font, width = 11, height = 2, borderwidth=1, relief="solid", command = reset)
rbtns[4].grid(row=4, column=0, ipadx = 61)

def send():

    global txtbox
    global cnt
    global resultPath

    txt = txtbox.get("1.0", "end")

    gmail_smtp = "smtp.gmail.com"  #gmail smtp 주소
    gmail_port = 465  #gmail smtp 포트번호
    smpt = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    my_id = "kko20-s2220204@gclass.ice.go.kr"
    my_password = "mtjz bmzt xidt mzqw"
    smpt.login(my_id, my_password)
    msg = MIMEMultipart()
    msg.set_charset('utf-8')
    msg["Subject"] = "마고4컷 사진 보내드립니다"
    msg["From"] = "마고4컷"
    msg["To"] = txt
    content = "안녕하세요 제어과 202 MDP 1조 마고4컷 사진 보내드립니다"
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    for i in range(cnt):

        image_name = resultPath[i]

        with open(image_name, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition','attachment', filename=image_name)
            msg.attach(img)
    to_mail = txt
    smpt.sendmail(my_id, txt, msg.as_string())  
    smpt.quit()

global txtbox

txtbox = tk.Text(tool_bar, font = font, width = 20, height = 2)
txtbox.grid(row=5)

sendBtn = tk.Button(tool_bar, text="사진 보내기", bg="white", font=font, width = 11, height = 1, borderwidth=1, relief="solid", command = send)
sendBtn.grid(row=6)

root.mainloop()