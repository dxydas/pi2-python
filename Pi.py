#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from Tkinter import *
#import tkMessageBox
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32
from time import gmtime, strftime
import math


IMUCanvasWidth = 312
IMUCanvasHeight = 100
widgetLength = 0.3*IMUCanvasHeight

def placeholderButton1Callback():
    messageBox.insert(END, "Click 1!\n")

def placeholderButton2Callback():
    messageBox.insert(END, "Click 2!\n")

def placeholderButton3Callback():
    messageBox.insert(END, "Click 3!\n")

def quit():
    root.destroy()

def fsrsListenerCallback(data):
    TMP=1

def messageBoxModifiedCallback(self):
    messageBox.see(END)
    messageBox.edit_modified(False)

def accelListenerCallback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.x)
    accelSliderX.set(data.x)
    accelSliderY.set(data.y)
    accelSliderZ.set(data.z)
    mu = 0.01
    signOfz = 1
    if (data.z < 0):
        signOfz = -1
    else:
        signOfz = 1
    accelRoll  = math.atan2( data.y, signOfz*math.sqrt(data.z*data.z + mu*data.x*data.x) );  # +-pi
    accelPitch = math.atan2( -data.x, math.sqrt(data.y*data.y + data.z*data.z) );            # +-pi/2
    #
    x0 = widgetLength*math.cos(accelRoll)
    y0 = widgetLength*math.sin(accelRoll)
    xOffset = 3+(1/6.0)*IMUCanvasWidth
    yOffset = 50
    IMUCanvas.delete("rollLine")
    rollLine = IMUCanvas.create_line(xOffset + x0, yOffset + y0,
                                     xOffset - x0, yOffset - y0,
                                     width = 5, fill = "red",
                                     tags = "rollLine")
    x0 = widgetLength*math.cos(accelPitch)
    y0 = widgetLength*math.sin(accelPitch)
    xOffset = 3+(1/2.0)*IMUCanvasWidth
    yOffset = 50
    IMUCanvas.delete("pitchLine")
    accelLine = IMUCanvas.create_line(xOffset + x0, yOffset + y0,
                                      xOffset - x0, yOffset - y0,
                                      width = 5, fill = "green",
                                      tags = "pitchLine")

def magnetListenerCallback(data):
    magnetSliderX.set(data.x)
    magnetSliderY.set(data.y)
    magnetSliderZ.set(data.z)

def headingListenerCallback(data):
    x0 = widgetLength*math.cos(math.pi/2.0 + data.data)
    y0 = widgetLength*math.sin(math.pi/2.0 + data.data)
    xOffset = 3+(5/6.0)*IMUCanvasWidth
    yOffset = 50
    IMUCanvas.delete("yawLine")
    yawLine = IMUCanvas.create_line(xOffset + x0, yOffset + y0,
                                    xOffset - x0, yOffset - y0,
                                    width = 5, fill = "blue",
                                    tags = "yawLine")

def gyroListenerCallback(data):
    gyroSliderX.set(data.x)
    gyroSliderY.set(data.y)
    gyroSliderZ.set(data.z)

def listener():
    rospy.init_node("listener", anonymous=True)

    topic_list = rospy.get_published_topics()
    if topic_list is None:
        #rospy.logerr("No topics found, quitting.")
        messageBox.insert(END, "No topics found, quitting.\n")
        return -1
    else:
        #rospy.loginfo("Subscribing to topics.")
        messageBox.insert(END, "Subscribing to topics.\n")
        for topic_name, topic_type in topic_list:
            if topic_name == "/fsrs":
                rospy.Subscriber(topic_name, Vector3, fsrsListenerCallback)
                FSRCanvasLabel.config(foreground="green")
            if topic_name == "/accel":
                rospy.Subscriber(topic_name, Vector3, accelListenerCallback)
                accelLabel.config(foreground="green")
                IMUCanvasLabelRoll.config(foreground="green")
                IMUCanvasLabelPitch.config(foreground="green")
            elif topic_name == "/magnet":
                rospy.Subscriber(topic_name, Vector3, magnetListenerCallback)
                magnetLabel.config(foreground="green")
            elif topic_name == "/heading":
                rospy.Subscriber(topic_name, Float32, headingListenerCallback)
                #IMUCanvasLabelHeading.config(foreground="green")
                IMUCanvasLabelYaw.config(foreground="green")
            elif topic_name == "/gyro":
                rospy.Subscriber(topic_name, Vector3, gyroListenerCallback)
                gyroLabel.config(foreground="green")
    #rospy.spin()
    return 0


startTime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

root = Tk()
root.title("Bioloid Sensors Visualiser")
root.resizable(width=FALSE, height=FALSE)
rootWidth = 480
rootHeight = 320
root.geometry("%dx%d" % (rootWidth, rootHeight))
#root.maxsize(width=440, height=300)
root.overrideredirect(True)  # Remove window decorations

#tkMessageBox.showinfo("Say Hello", "Hello World")

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

topframe = Frame(root)
#topframe = LabelFrame(root, text="IMU")
topframe.grid(row=0, column=0, sticky=N+S+W+E)

bottomframe = Frame(root)
bottomframe.grid(row=1, column=0, sticky=N+S+W+E)

Grid.rowconfigure(topframe, 0, weight=1)
Grid.columnconfigure(topframe, 0, weight=1)
Grid.rowconfigure(bottomframe, 0, weight=1)
Grid.columnconfigure(bottomframe, 0, weight=1)

topleftsubframe = Frame(topframe)
bottomleftsubframe = Frame(topframe)
toprightsubframe = Frame(topframe)
bottomrightsubframe = Frame(topframe)

topleftsubframe.grid(row=0, column=0, sticky=W)
bottomleftsubframe.grid(row=1, column=0, sticky=W)
toprightsubframe.grid(row=0, column=1, sticky=E)
bottomrightsubframe.grid(row=1, column=1, sticky=E)

#topleftlabel = Label(topleftsubframe, text="topleft")
#topleftlabel.grid(row=0, column=0)
#bottomleftlabel = Label(bottomleftsubframe, text="bottomleft")
#bottomleftlabel.grid(row=0, column=0)
#toprightlabel = Label(toprightsubframe, text="topright")
#toprightlabel.grid(row=0, column=1)
#bottomrightlabel = Label(bottomrightsubframe, text="bottomright")
#bottomrightlabel.grid(row=5, column=0)


FSRCanvasLabel = Label(topleftsubframe, text="FSRs", foreground="red")
FSRCanvasLabel.grid(row=0, column=0)
FSRCanvas = Canvas(topleftsubframe, background="#CCFFFF", width=120, height=60)
FSRCanvas.grid(row=1, column=0)

testVal = 500 * 255/1023.0
colG = "%02x" % (255 - testVal)
FSRCanvas.create_rectangle(1, 1, 30, 30, fill="#" + "FF" + colG + "00")
FSRCanvas.create_text(15, 15, text="0")
#
testVal = 1023 * 255/1023.0
colG = "%02x" % (255 - testVal)
FSRCanvas.create_rectangle(30, 1, 60, 30, fill="#" + "FF" + colG + "00")
#
testVal = 0 * 255/1023.0
colG = "%02x" % (255 - testVal)
FSRCanvas.create_rectangle(30, 30, 60, 60, fill="#" + "FF" + colG + "00")

placeholderButton1 = Button(bottomleftsubframe, text="Button 1", command=placeholderButton1Callback)
placeholderButton1.grid(row=0, column=0)
placeholderButton2 = Button(bottomleftsubframe, text="Button 2", command=placeholderButton2Callback)
placeholderButton2.grid(row=1, column=0)
placeholderButton3 = Button(bottomleftsubframe, text="Button 3", command=placeholderButton3Callback)
placeholderButton3.grid(row=2, column=0)

IMUCanvasLabelRoll = Label(toprightsubframe, text="Roll", foreground="red")
IMUCanvasLabelRoll.grid(row=0, column=0)
IMUCanvasLabelPitch = Label(toprightsubframe, text="Pitch", foreground="red")
IMUCanvasLabelPitch.grid(row=0, column=1)
IMUCanvasLabelYaw = Label(toprightsubframe, text="Yaw", foreground="red")
IMUCanvasLabelYaw.grid(row=0, column=2)
#IMUCanvasLabelHeading = Label(toprightsubframe, text="Heading", foreground="red")
#IMUCanvasLabelHeading.grid(row=0, column=3)
IMUCanvas = Canvas(toprightsubframe, background="#FFFF66", width=IMUCanvasWidth, height=IMUCanvasHeight)
IMUCanvas.grid(row=1, column=0, columnspan=3)

#IMUCanvas.create_line(0, 50, 69, 50, width = 5, fill = "red")
#IMUCanvas.create_line(70, 50, 139, 50, width = 5, fill = "green")
#IMUCanvas.create_line(140, 50, 209, 50, width = 5, fill = "blue")
#IMUCanvas.create_line(210, 50, 280, 50, width = 5, fill = "orange")
#IMUCanvas.create_line(245, 16+0, 245, 16+69, width = 5, fill = "orange")

IMUCanvas.create_text(3+(1/6.0)*IMUCanvasWidth, 10, text="0")
IMUCanvas.create_text(3+(1/2.0)*IMUCanvasWidth, 10, text="0")
IMUCanvas.create_text(3+(5/6.0)*IMUCanvasWidth, 10, text="0")
#IMUCanvas.create_text(245, 10, text="0.0")

labelX = Label(bottomrightsubframe, text="X")
labelX.grid(row=1, column=0)
labelY = Label(bottomrightsubframe, text="Y")
labelY.grid(row=2, column=0)
labelZ = Label(bottomrightsubframe, text="Z")
labelZ.grid(row=3, column=0)

accelLabel = Label(bottomrightsubframe, text="Accel", foreground="red")
accelLabel.grid(row=0, column=1)
accelSliderX = Scale(bottomrightsubframe, from_=-2.0, to=2.0, resolution=0.0001, orient=HORIZONTAL)
accelSliderX.grid(row=1, column=1)
accelSliderY = Scale(bottomrightsubframe, from_=-2.0, to=2.0, resolution=0.0001, orient=HORIZONTAL)
accelSliderY.grid(row=2, column=1)
accelSliderZ = Scale(bottomrightsubframe, from_=-2.0, to=2.0, resolution=0.0001, orient=HORIZONTAL)
accelSliderZ.grid(row=3, column=1)

magnetLabel = Label(bottomrightsubframe, text="Magnet", foreground="red")
magnetLabel.grid(row=0, column=2)
magnetSliderX = Scale(bottomrightsubframe, from_=-4000.0, to=4000.0, resolution=1, orient=HORIZONTAL)
magnetSliderX.grid(row=1, column=2)
magnetSliderY = Scale(bottomrightsubframe, from_=-4000.0, to=4000.0, resolution=1, orient=HORIZONTAL)
magnetSliderY.grid(row=2, column=2)
magnetSliderZ = Scale(bottomrightsubframe, from_=-4000.0, to=4000.0, resolution=1, orient=HORIZONTAL)
magnetSliderZ.grid(row=3, column=2)

gyroLabel = Label(bottomrightsubframe, text="Gyro", foreground="red")
gyroLabel.grid(row=0, column=3)
gyroSliderX = Scale(bottomrightsubframe, from_=-1.0, to=1.0, resolution=0.0001, orient=HORIZONTAL)
gyroSliderX.grid(row=1, column=3)
gyroSliderY = Scale(bottomrightsubframe, from_=-1.0, to=1.0, resolution=0.0001, orient=HORIZONTAL)
gyroSliderY.grid(row=2, column=3)
gyroSliderZ = Scale(bottomrightsubframe, from_=-1.0, to=1.0, resolution=0.0001, orient=HORIZONTAL)
gyroSliderZ.grid(row=3, column=3)

#headingLabel = Label(bottomrightsubframe, text="Heading", foreground="red")
#headingLabel.grid(row=0, column=4)
#headingValue = Label(bottomrightsubframe, text="0.0")
#headingValue.grid(row=1, column=4)

messageBox = Text(bottomframe, height=3)
messageBox.grid(row=0, column=0, sticky=N+S+W+E)
scrl = Scrollbar(bottomframe, command=messageBox.yview)
scrl.grid(row=0, column=1, sticky=N+S)
messageBox.config(yscrollcommand=scrl.set)
messageBox.bind("<<Modified>>", messageBoxModifiedCallback)
messageBox.insert(END, "Started at: " + startTime + "\n")

#b = Button(bottomframe, text="OK", command=buttonCallback)
#b.grid(row=0, column=0)

quitButton = Button(bottomframe, text="Quit", command=quit)
quitButton.grid(row=0, column=2)


if __name__ == '__main__':
    listener()
    mainloop()

