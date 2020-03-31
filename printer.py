import constant
import config
from Adafruit_Thermal import *
import logging
import image_and_text
from PIL import Image, ImageTk

active_printer = None

class Printer(Adafruit_Thermal):
  def print_text(self, file_path):
      with open(file_path, 'r') as myfile:
        text = myfile.read()
        self.justify('C')
        self.println(text)

  def print_photo(self, file_path):
      photo = Image.open(file_path)
      width, height = photo.size
      if height > width:
          newWidth = config.MAX_PAPER_PIXEL_LENGTH
          newHeight = height * config.MAX_PAPER_PIXEL_LENGTH / width
      else:
          newHeight = config.MAX_PAPER_PIXEL_LENGTH
          newWidth = width * config.MAX_PAPER_PIXEL_LENGTH / height
      photo = photo.resize((newWidth, newHeight), Image.ANTIALIAS)
      # Apply B&W
      photo = photo.convert('1')
      self.printImage(photo, True)
      self.feed(3)

  def start():
      global active_printer
      active_printer = Printer(config.PORT, config.BAUDRATE, timeout=5)
      active_printer.wake()

class Fake_printer(Adafruit_Thermal):
  def __init__(self):
      logging.info("Faked printer initialized")

  def print_text(self, file_path):
      file_path = image_and_text.get_file_path()
      with open(file_path, 'r') as myfile:
        text = myfile.read()
        logging.info("Printing : %s", text)

  def print_photo(self, file_path):
      logging.info("Printing image : %s", file_path)

  @staticmethod
  def start():
      global active_printer
      active_printer = Fake_printer()

def print_item():
    global active_printer
    logging.info("Printing item")
    file_path = image_and_text.get_file_path()
    file_type = image_and_text.get_file_type(file_path)
    if file_type == constant.IMAGE_TYPE:
        active_printer.print_photo(file_path)
    elif file_type == constant.TEXT_TYPE:
        active_printer.print_text(file_path)

