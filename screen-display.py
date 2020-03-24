#################################################################################################
# Imports Section                                                                               #
#################################################################################################
import Tkinter as tk
from PIL import Image, ImageTk
import glob
import time
import threading
import os
from Adafruit_Thermal import *
#import RPI.GPIO as GPIO

#################################################################################################
# Defines Section                                                                               #
#################################################################################################
SIZE = (480, 320)
#SIZE = (1440, 900)
PATH = "/home/pi/projet/git/secret/data/*/*/*/*"
#PATH = "/Users/Pikachu/Desktop/FEFE/2018/*/*/*"


FILE_UPDATE_DELAY = 20
INCREMENT = 1
DECREMENT = -1
ENTERING  = 0

PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

# Paper width is 384 pixel
MAX_PAPER_PIXEL_LENGTH = 384

#################################################################################################
# Buttons Section                                                                               #
#################################################################################################
def create_enter_button(canvas, root):
    global enter_button
    enter_button = tk.Button(root, text = "ENTER", command = enter_button_callback, width = 5)
    enter_button_window = canvas.create_window(SIZE[0]/2, SIZE[1]/2, anchor='center', window=enter_button)

def create_left_button(canvas, root):
    left_button = tk.Button(root, text = "<", command = get_older_item, width = 1)
    left_button_window = canvas.create_window(0, SIZE[1]/2, anchor='w', window=left_button)

def create_right_button(canvas, root):
    right_button = tk.Button(root, text = ">", command = get_newer_item, width = 1)
    right_button_window = canvas.create_window(SIZE[0], SIZE[1]/2, anchor='e', window=right_button)

def create_quit_button(canvas, root):
    quit_button = tk.Button(root, text = "Quit", command = print_item, width = 10)
    quit_button_window = canvas.create_window(SIZE[0]/2, SIZE[1], anchor='s', window=quit_button)

text = None
enter_button = None
def remove_old_view_elements():
    global text, enter_button
    if enter_button:
        print ("destroying button")
        enter_button.destroy()
    if text:
        text.destroy()
    canvas.delete('item')

#################################################################################################
# Callbacks Section                                                                             #
#################################################################################################
def enter_button_callback():
    load_file_list()
    update_file_index(ENTERING)
    display_file()

def get_newer_item():
    update_file_index(DECREMENT)
    display_file()

def get_older_item():
    update_file_index(INCREMENT)
    display_file()

def new_message_event(*args):
    global canvas, root
    #led_trigger_effect("true")
    create_enter_button(canvas, root)

def print_item():
    file_path = get_file_path()
    file_type = get_file_type(file_path)
    if file_type == "PHOTO":
        print_photo()
    elif file_type == "TEXT":
        print_text()

def print_text():
    file_path = get_file_path()
    with open(file_path, 'r') as myfile:
      texte = myfile.read()
      printer.justify('C')
      printer.println(texte)

def print_photo():
    file_path = get_file_path()
    photo = Image.open(file_path)
    width, height = photo.size
    if height > width:
        newWidth = MAX_PAPER_PIXEL_LENGTH
        newHeight = height * MAX_PAPER_PIXEL_LENGTH / width
    else:
        newHeight = MAX_PAPER_PIXEL_LENGTH
        newWidth = width * MAX_PAPER_PIXEL_LENGTH / height
    photo = photo.resize((newWidth, newHeight), Image.ANTIALIAS)
    # Apply B&W 
    photo = photo.convert('1')
    printer.printImage(photo, True)
    printer.feed(3)



#################################################################################################
# File Section                                                                                  #
#################################################################################################
def get_file_type(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == ".jpg":
        return "PHOTO"
    elif file_extension == ".txt":
        return "TEXT"
    else:
        return "UNKNOWN"

def display_file():
    file_path = get_file_path()
    file_type = get_file_type(file_path)
    remove_old_view_elements()
    # stop effects
    #led_trigger_effect("stop")
    trigger_motor_effect = True
    if file_type == "PHOTO":
       display_photo(file_path)
    elif file_type == "TEXT":
       display_text(file_path)

def update_file_index(step):
    global file_index, file_list
    if step == INCREMENT and file_index < len(file_list) - 1:
        file_index = file_index + 1
    elif step == DECREMENT and file_index > 0:
        file_index = file_index - 1
    elif step == ENTERING:
        file_index = 0

def load_file_list():
    global file_list
    file_list = sorted(glob.glob(PATH))
    file_list.reverse()

def get_file_path():
    global file_index, file_list
    return file_list[file_index]

#################################################################################################
# Thread Section                                                                                  #
#################################################################################################
def file_watching_thread():
    global root
    before = dict ([(f, None) for f in glob.glob(PATH)])
    while True:
      print ("loop")
      time.sleep (FILE_UPDATE_DELAY)
      after = dict ([(f, None) for f in glob.glob(PATH)])
      added = [f for f in after if not f in before]
      if added:
          print ("New file")
          root.event_generate("<<NewMessage>>", when="tail")
      before = after

#LEDPIN = 12  
#LED_UPDATE_DELAY = 20
#trigger_led_effect = False
#def led_effect_thread():
#    global trigger_led_effect
#    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
#    GPIO.setup(LEDPIN, GPIO.OUT)   # Set LedPin's mode is output
#    GPIO.output(LEDPIN, GPIO.LOW)  # Set LedPin to low(0V)
#
#    p = GPIO.PWM(LEDPIN, 1000)     # set Frequece to 1KHz
#    p.start(0)                     # Duty Cycle = 0
#    while True:
#        time.sleep(LED_UPDATE_DELAY)
#        while trigger_led_effect:
#            for dc in range(0, 101, 4):   # Increase duty cycle: 0~100
#                p.ChangeDutyCycle(dc)     # Change duty cycle
#                time.sleep(0.05)
#            time.sleep(1)
#            for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
#                p.ChangeDutyCycle(dc)
#                time.sleep(0.05)
#            time.sleep(1)
#
#
#def motor_effect_thread():
#    global trigger_motor_effect
#    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
#    GPIO.setup(MOTORPIN, GPIO.OUT)   # Set LedPin's mode is output
#    GPIO.output(MOTORPIN, GPIO.LOW)  # Set LedPin to low(0V)
#    while True:
#        time.sleep(MOTOR_UPDATE_DELAY)
#        if trigger_motor_effect:
#            GPIO.output(MOTORPIN, GPIO.HIGH)
#            time.sleep(MOTOR_EFFECT_DELAY)
#            GPIO.output(MOTORPIN, GPIO.LOW) 
#            trigger_motor_effect = False
#


def trigger_effect(command):
    pass
    # global trigger_led_effect
    # if command == "start":
    #     trigger_led_effect = True
    # elif command == "stop":
    #     trigger_led_effect = False

#################################################################################################
# Photo Section                                                                                 #
#################################################################################################
# for data persistency
photo = 0
def display_photo(img_path):
    global photo, canvas
    tmp_photo = Image.open(img_path).resize(SIZE)
    photo = ImageTk.PhotoImage(tmp_photo)
    canvas.create_image(0, 0, anchor="nw", image=photo, tags=('item'))

#################################################################################################
# Text Message Section                                                                          #
#################################################################################################
# for data persistency
texte = 0
def display_text(text_path):
    global text, canvas
    with open(text_path, 'r') as myfile:
      texte = myfile.read()

    text = tk.Text(root, width=60, height=20)
    text.tag_configure('tag-center', justify='center', wrap='word')
    text.insert(tk.INSERT, texte, 'tag-center')
    text["state"] = tk.DISABLED
    text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


#################################################################################################
# Main Section                                                                                 #
#################################################################################################
printer = Adafruit_Thermal(PORT, BAUDRATE, timeout=5)
printer.wake()

file_watching = threading.Thread(target=file_watching_thread)
#led_effect = threading.Thread(target=led_effect_thread)

file_watching.start()
#led_effect.start()

# Init
root = tk.Tk()
# For fullscreen
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)
root.geometry('480x320')
#root.geometry('1440x900')

# For new message event
root.bind("<<NewMessage>>", new_message_event)

# Display
canvas = tk.Canvas(root, width=SIZE[0], height=SIZE[1])
canvas.pack()

create_left_button(canvas, root)
create_right_button(canvas, root)
create_quit_button(canvas, root)

# GLOBAL VARIABLES
file_index = 0
file_list = None
load_file_list()

display_file()

# Display
root.mainloop()
