import constant
import config
import Tkinter as tk
from PIL import Image, ImageTk
import logging

class Gui(tk.Canvas):
  # For data persistency displayed data need to be stored in global variable or it will be destroyed
  text_element = None
  text_persistent = None
  photo_persistent = 0

  # We need to keep track of this button so that we can destroy it later
  new_item = None

  def create_left_button(self, root, command):
    left_button = tk.Button(root, text = "<", command = command, width = 1, relief="flat")
    left_button_window = self.create_window(0, config.SCREEN["HEIGHT"]/2, anchor='w',
    window=left_button)

  def create_right_button(self, root, command):
    right_button = tk.Button(root, text = ">", command = command, width = 1, relief="flat")
    right_button_window = self.create_window(config.SCREEN["WIDTH"], config.SCREEN["HEIGHT"]/2,
    anchor='e', window=right_button)

  def create_print_button(self, root, command):
    print_button = tk.Button(root, text = "Print", command = command, width = 10, relief="flat")
    print_button_window = self.create_window(config.SCREEN["WIDTH"]/2, config.SCREEN["HEIGHT"]-10,
    anchor='s', window=print_button)

  def create_new_item_button(self, root, command):
    Gui.new_item = tk.Button(root, text = "Display new message", command = command, width = 5, relief="flat")
    new_item_button_window = self.create_window(config.SCREEN["WIDTH"]/2,
    config.SCREEN["HEIGHT"]/2, anchor='center', window=Gui.new_item)


  def display_text(self, text_path):
      with open(text_path, 'r') as myfile:
        text_persistent = myfile.read()

      Gui.text_element = tk.Text(self, width=60, height=0, relief="flat")
      Gui.text_element.tag_configure('tag-center', justify='center', wrap='word')
      Gui.text_element.insert(tk.INSERT, text_persistent, 'tag-center')
      Gui.text_element["state"] = tk.DISABLED
      Gui.text_element.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

  def display_photo(self, img_path):
      global photo_persistent
      photo_tmp = Image.open(img_path).resize(constant.SCREEN_SIZE)
      photo_persistent = ImageTk.PhotoImage(photo_tmp)
      self.create_image(0, 0, anchor="nw", image=photo_persistent, tags=('item'))

  def remove_old_view_elements(self):
      if Gui.new_item:
          logging.debug("New_item button is present, destroying it")
          Gui.new_item.destroy()
          Gui.new_item = None
      if Gui.text_element:
          logging.debug("Text_element is present, destroying it")
          Gui.text_element.destroy()
          Gui.text_element = None
      self.delete('item')

