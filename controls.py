#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import RPi.GPIO as GPIO


class Buttons():

    # === Button Click Event Handler ============================================

    def handler(buttonDictionary, e):

        # print(' DEBUG: ' + e + ' was clicked ')

        if e == 'shutterUp':
            buttonDictionary.update({'shutterUp': True})
        elif e == 'shutterDown':
            buttonDictionary.update({'shutterDown': True})
        elif e == 'isoUp':
            buttonDictionary.update({'isoUp': True})
        elif e == 'isoDown':
            buttonDictionary.update({'isoDown': True})
        elif e == 'evUp':
            buttonDictionary.update({'evUp': True})
        elif e == 'evDown':
           buttonDictionary.update({'evDown': True})
        elif e == 'bracketUp':
            buttonDictionary.update({'bracketUp': True})
        elif e == 'bracketDown':
            buttonDictionary.update({'bracketDown': True})
        elif e == 'videoMode':
            buttonDictionary.update({'videoMode': True})
        elif e == 'capture':
            buttonDictionary.update({'capture': True})
        elif e == 'captureVideo':
            buttonDictionary.update({'captureVideo': True})
        elif e == 'exit':
            buttonDictionary.update({'exit': True})                 

        time.sleep(0.2)

        return buttonDictionary
    


class HWControls():

    def hw_handler(channel, buttonDictionary, e):

        # print(' DEBUG: ' + e + ' was clicked ')

        if e == 'capture':
            buttonDictionary.update({'capture': True})
        elif e == 'init_shutdown':
            buttonDictionary.update({'init_shutdown': True})                        
        elif e == 'verify_shutdown':
            buttonDictionary.update({'verify_shutdown': True})                      

        time.sleep(0.2)
        return buttonDictionary

    def update_battery_gauge(channel, level, p1, p2, p3):
        level = int(str(GPIO.input(p1))+str(GPIO.input(p2))+str(GPIO.input(p3)))

        if level < 2:
            time.sleep(2)
            if level < 2:
                print("would shutdown now level:"+str(level))
                #os.system("sudo shutdown -h now")

        time.sleep(0.2)
        return level

    def create(self, buttonDictionary, level):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #Power button
        GPIO.setup(3, GPIO.IN)
        GPIO.add_event_detect(3, GPIO.FALLING, bouncetime=2000, callback=lambda x: self.hw_handler(buttonDictionary, 'init_shutdown'))
        #GPIO.add_event_detect(3, GPIO.RISING, callback=lambda: Buttons.handler(buttonDictionary, 'verify_shutdown'), bouncetime=2000)

        #Battery gauge
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(22, GPIO.BOTH, bouncetime=200, callback=lambda x: self.update_battery_gauge(level, 24, 23, 22))
        GPIO.add_event_detect(23, GPIO.BOTH, bouncetime=200, callback=lambda x: self.update_battery_gauge(level, 24, 23, 22))
        GPIO.add_event_detect(24, GPIO.BOTH, bouncetime=200, callback=lambda x: self.update_battery_gauge(level, 24, 23, 22))

        #Shutter button
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(26, GPIO.FALLING, bouncetime=200, callback=lambda x: self.hw_handler(buttonDictionary, 'capture'))


class OnScreenControls():

    # === Create Controls =======================================================

    def create(self, running, statusDictionary, buttonDictionary):

        currentDirectory = '/home/pi/Pieca-camera-software/'
        num_buttons = 6
        messageHeight = 20

        root = tk.Tk()
        root.title('Camera Controls')
        root.wm_attributes('-type', 'splash')
        root.geometry(str(root.winfo_screenwidth()-816) + 'x' + str(root.winfo_screenheight()) + '+816+0')
        root['background'] = '#111111'


        # --- On-Screen Control Button Styles -----------------------------------

        buttonStyle = ttk.Style()
        buttonStyle.configure('default.TButton', background = '#a6a6a6', bordercolor = '#111111', borderwidth=0)
        buttonStyle.configure('warning.TButton', background='#cc0000', bordercolor = '#880000', borderwidth=0)
        buttonStyle.configure('primary.TButton', background = '#00DDF1', bordercolor = '#00DDF1', borderwidth=0)
        buttonWidth = (root.winfo_screenwidth()-816)/2
        buttonHeight = ((root.winfo_screenheight()-messageHeight)/num_buttons) - (((root.winfo_screenheight()-messageHeight)/num_buttons)/6)


        # --- On-Screen Control Label Styles ------------------------------------

        labelStyle = ttk.Style()
        labelStyle.configure('default.TLabel', background='#808080', foreground='#EEEEEE')
        labelStyle.configure('warning.TLabel', background='#880000', foreground='#EEEEEE')
        labelStyle.configure('primary.TLabel', background='#00bbcc', foreground='#111111')
        labelHeight = (((root.winfo_screenheight()-messageHeight)/num_buttons)/6)

        borderLeft = 0

        # --- Control Rendering -------------------------------------------------
        # Status
        windowWidth = root.winfo_screenwidth()-816-45
        statusVariable = tk.StringVar() 
        statusLabel = ttk.Label(root, compound=tk.CENTER, textvariable=statusVariable)
        statusLabel['style'] = 'default.TLabel'
        statusLabel.configure(anchor='center')
        statusVariable.set(statusDictionary['message'])         
        statusLabel.place(x=0,y=root.winfo_screenheight()-messageHeight,width=windowWidth,height=messageHeight)

        # Battery
        batteryVariable = tk.StringVar() 
        batteryLabel = ttk.Label(root, compound=tk.CENTER, textvariable=batteryVariable)
        batteryLabel['style'] = 'primary.TLabel'
        batteryLabel.configure(anchor='center')
        batteryVariable.set(statusDictionary['battery'])         
        batteryLabel.place(x=windowWidth,y=root.winfo_screenheight()-messageHeight,width=45,height=messageHeight)

        # Exit
        image = Image.open(os.path.join(currentDirectory, 'images/exit.png'))
        exitImage = ImageTk.PhotoImage(image)
        exitButton = ttk.Button(root, compound=tk.CENTER, image=exitImage, command=lambda: Buttons.handler(buttonDictionary, 'exit'))
        exitButton['style'] = 'warning.TButton'
        exitButton.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*1,width=buttonWidth,height=buttonHeight)

        exitLabel = ttk.Label(root, compound=tk.CENTER, text='Exit')
        exitLabel['style'] = 'warning.TLabel'
        exitLabel.configure(anchor='center')
        exitLabel.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*1+buttonHeight,width=buttonWidth,height=labelHeight)


        # Capture Video
        image = Image.open(os.path.join(currentDirectory, 'images/capture-video.png'))
        captureVideoImage = ImageTk.PhotoImage(image)
        captureVideoButton = ttk.Button(root, compound=tk.CENTER, image=captureVideoImage, command=lambda: Buttons.handler(buttonDictionary, 'captureVideo'))
        captureVideoButton['style'] = 'primary.TButton'
        captureVideoButton.place(x=borderLeft,y=0,width=buttonWidth,height=buttonHeight)

        captureVideoLabel = ttk.Label(root, compound=tk.CENTER, text='Record')
        captureVideoLabel['style'] = 'primary.TLabel'
        captureVideoLabel.configure(anchor='center')
        captureVideoLabel.place(x=borderLeft,y=buttonHeight,width=buttonWidth,height=labelHeight)

        # Video Mode
        image = Image.open(os.path.join(currentDirectory, 'images/video-mode.png'))
        videoModeImage = ImageTk.PhotoImage(image)
        videoModeButton = ttk.Button(root, compound=tk.CENTER, image=videoModeImage, command=lambda: Buttons.handler(buttonDictionary, 'videoMode'))
        videoModeButton['style'] = 'default.TButton'
        videoModeButton.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*1,width=buttonWidth,height=buttonHeight)

        videoModeLabel = ttk.Label(root, compound=tk.CENTER, text='Mode')
        videoModeLabel['style'] = 'default.TLabel'
        videoModeLabel.configure(anchor='center')
        videoModeLabel.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*1+buttonHeight,width=buttonWidth,height=labelHeight)


        # Shutter Speed 
        image = Image.open(os.path.join(currentDirectory, 'images/shutter-speed-up.png'))
        shutterUpImage = ImageTk.PhotoImage(image)
        shutterUpButton = ttk.Button(root, compound=tk.CENTER, image=shutterUpImage, command=lambda: Buttons.handler(buttonDictionary, 'shutterUp'))
        shutterUpButton['style'] = 'default.TButton'
        shutterUpButton.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*2,width=buttonWidth,height=buttonHeight)

        image = Image.open(os.path.join(currentDirectory, 'images/shutter-speed-down.png'))
        shutterDownImage = ImageTk.PhotoImage(image)
        shutterDownButton = ttk.Button(root, compound=tk.CENTER, image=shutterDownImage, command=lambda: Buttons.handler(buttonDictionary, 'shutterDown'))
        shutterDownButton['style'] = 'default.TButton'
        shutterDownButton.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*2,width=buttonWidth,height=buttonHeight)

        shutterLabel = ttk.Label(root, compound=tk.CENTER, text='Shutter Speed')
        shutterLabel['style'] = 'default.TLabel'
        shutterLabel.configure(anchor='center')
        shutterLabel.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*2+buttonHeight,width=buttonWidth*2,height=labelHeight)


        #ISO
        image = Image.open(os.path.join(currentDirectory, 'images/iso-up.png'))
        isoUpImage = ImageTk.PhotoImage(image)
        isoUpButton = ttk.Button(root, compound=tk.CENTER, image=isoUpImage, command=lambda: Buttons.handler(buttonDictionary, 'isoUp'))
        isoUpButton['style'] = 'default.TButton'
        isoUpButton.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*3,width=buttonWidth,height=buttonHeight)

        image = Image.open(os.path.join(currentDirectory, 'images/iso-down.png'))
        isoDownImage = ImageTk.PhotoImage(image)
        isoDownButton = ttk.Button(root, compound=tk.CENTER, image=isoDownImage, command=lambda: Buttons.handler(buttonDictionary, 'isoDown'))
        isoDownButton['style'] = 'default.TButton'
        isoDownButton.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*3,width=buttonWidth,height=buttonHeight)

        isoLabel = ttk.Label(root, compound=tk.CENTER, text='ISO')
        isoLabel['style'] = 'default.TLabel'
        isoLabel.configure(anchor='center')
        isoLabel.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*3+buttonHeight,width=buttonWidth*2,height=labelHeight)


        # Exposure Compensation
        image = Image.open(os.path.join(currentDirectory, 'images/exposure-compensation-up.png'))
        evUpImage = ImageTk.PhotoImage(image)
        evUpButton = ttk.Button(root, compound=tk.CENTER, image=evUpImage, command=lambda: Buttons.handler(buttonDictionary, 'evUp'))
        evUpButton['style'] = 'default.TButton'
        evUpButton.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*4,width=buttonWidth,height=buttonHeight)

        image = Image.open(os.path.join(currentDirectory, 'images/exposure-compensation-down.png'))
        evDownImage = ImageTk.PhotoImage(image)
        evDownButton = ttk.Button(root, compound=tk.CENTER, image=evDownImage, command=lambda: Buttons.handler(buttonDictionary, 'evDown'))
        evDownButton['style'] = 'default.TButton'
        evDownButton.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*4,width=buttonWidth,height=buttonHeight)

        evLabel = ttk.Label(root, compound=tk.CENTER, text='Compensation')
        evLabel['style'] = 'default.TLabel'
        evLabel.configure(anchor='center')
        evLabel.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*4+buttonHeight,width=buttonWidth*2,height=labelHeight)


        # Exposure Bracketing
        image = Image.open(os.path.join(currentDirectory, 'images/exposure-bracketing-up.png'))
        bracketUpImage = ImageTk.PhotoImage(image)
        bracketUpButton = ttk.Button(root, compound=tk.CENTER, image=bracketUpImage, command=lambda: Buttons.handler(buttonDictionary, 'bracketUp'))
        bracketUpButton['style'] = 'default.TButton'
        bracketUpButton.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*5,width=buttonWidth,height=buttonHeight)

        image = Image.open(os.path.join(currentDirectory, 'images/exposure-bracketing-down.png'))
        bracketDownImage = ImageTk.PhotoImage(image)
        bracketDownButton = ttk.Button(root, compound=tk.CENTER, image=bracketDownImage, command=lambda: Buttons.handler(buttonDictionary, 'bracketDown'))
        bracketDownButton['style'] = 'default.TButton'
        bracketDownButton.place(x=borderLeft+(buttonWidth*1),y=(buttonHeight+labelHeight)*5,width=buttonWidth,height=buttonHeight)

        bracketLabel = ttk.Label(root, compound=tk.CENTER, text='Bracketing')
        bracketLabel['style'] = 'default.TLabel'
        bracketLabel.configure(anchor='center')
        bracketLabel.place(x=borderLeft+(buttonWidth*0),y=(buttonHeight+labelHeight)*5+buttonHeight,width=buttonWidth*2,height=labelHeight)


        # Capture
        image = Image.open(os.path.join(currentDirectory, 'images/capture-photo.png'))
        captureImage = ImageTk.PhotoImage(image)
        captureButton = ttk.Button(root, compound=tk.CENTER, image=captureImage, command=lambda: Buttons.handler(buttonDictionary, 'capture'))
        captureButton['style'] = 'primary.TButton'
        captureButton.place(x=borderLeft+(buttonWidth*1),y=0,width=buttonWidth,height=buttonHeight)

        captureLabel = ttk.Label(root, compound=tk.CENTER, text='Capture')
        captureLabel['style'] = 'primary.TLabel'
        captureLabel.configure(anchor='center')
        captureLabel.place(x=borderLeft+(buttonWidth*1),y=buttonHeight,width=buttonWidth,height=labelHeight)


        def updateStatus():
            statusVariable.set(statusDictionary['message'])
            if statusDictionary['action'] == 'recording' and captureVideoLabel['style'] == 'primary.TLabel':
                captureVideoLabel['style'] = 'warning.TLabel'
            elif statusDictionary['action'] == 'recording' and captureVideoLabel['style'] == 'warning.TLabel':
                captureVideoLabel['style'] = 'primary.TLabel'
            else:
                captureVideoLabel['style'] = 'primary.TLabel'

            batteryVariable.set(statusDictionary['battery'])

            if running == False:
                root.destroy()
                sys.exit(0)
            root.after(500, updateStatus)
            

        root.after(500, updateStatus)

        # --- Create Controls ---------------------------------------------------

        root.mainloop()
