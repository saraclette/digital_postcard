import constant
import config
from gui import Gui
import image_and_text
import Tkinter as tk
import threading
import time
import logging
import printer
import effect
import glob

def screen_update_thread():
    while True:
      image_and_text.file_has_changed_lock.acquire()
      if image_and_text.file_has_changed == True:
        canvas.remove_old_view_elements()
        image_and_text.display_file(canvas)
        image_and_text.file_has_changed = False
      image_and_text.file_has_changed_lock.release()

      time.sleep(constant.SCREEN_UPDATE_DELAY)

def new_item_monitor_thread():
    old_file_list = dict([(f, None) for f in glob.glob(config.PATH)])
    while True:
      new_file_list = dict([(f, None) for f in glob.glob(config.PATH)])
      new_file = [f for f in new_file_list if not f in old_file_list]
      if new_file:
          logging.info("New file : %s was found", new_file)
          root.event_generate(constant.SHOW_NEW_ITEM_EVENT, when="tail")
      old_file_list = new_file_list
      time.sleep(constant.NEW_ITEM_MONITOR_DELAY)

def new_item_event(*args):
  canvas.create_new_item_button(root, image_and_text.display_new_item)
  effect.trigger_effect(constant.ALL_EFFECT_TARGET, constant.START_COMMAND)

def get_older_item():
  image_and_text.get_older_item()
  effect.trigger_effect(constant.LED_EFFECT_TARGET, constant.STOP_COMMAND)

def get_newer_item():
  image_and_text.get_newer_item()
  effect.trigger_effect(constant.LED_EFFECT_TARGET, constant.STOP_COMMAND)

def display_new_item():
  image_and_text.display_new_item()
  effect.trigger_effect(constant.LED_EFFECT_TARGET, constant.STOP_COMMAND)


if __name__ == "__main__":
  # Initialization
  logging.basicConfig(level=logging.DEBUG)
  printer.Fake_printer.start()

  root = tk.Tk()
  root.attributes('-fullscreen',True)

  canvas = Gui(root, width=config.SCREEN["WIDTH"], height=config.SCREEN["HEIGHT"])
  canvas.pack()

  image_and_text.load_file_list()
  image_and_text.display_file(canvas)

  # For new item event
  root.bind(constant.SHOW_NEW_ITEM_EVENT, new_item_event)

  # Gui elements creation
  canvas.create_left_button(root, get_older_item)
  canvas.create_right_button(root, get_newer_item)
  canvas.create_print_button(root, printer.print_item)

  # Threads definition
  screen_update = threading.Thread(target=screen_update_thread)
  new_item_monitor = threading.Thread(target=new_item_monitor_thread)
  led_effect = threading.Thread(target=effect.led_effect_thread)
  motor_effect = threading.Thread(target=effect.motor_effect_thread)

  # Threads launch
  screen_update.start()
  new_item_monitor.start()

  if config.USE_EFFECT:
    led_effect.start()
    motor_effect.start()

  # Gui launch
  root.mainloop()
