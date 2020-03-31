import constant
import config
import glob
import os
import gui
import logging
import Lock

file_has_changed = False
file_has_changed_lock = Lock()

file_index = 0
file_list = []

def get_file_type(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension in constant.IMAGE_EXTENSION_LIST:
        logging.debug("file type is image")
        return constant.IMAGE_TYPE
    elif file_extension in constant.TEXT_EXTENSION_LIST:
        logging.debug("file type is text")
        return constant.TEXT_TYPE
    else:
        logging.error("file type is unknown")
        return constant.UNKNOWN_TYPE

def get_file_path():
    global file_index, file_list
    return file_list[file_index]

def display_file(canvas):
    file_path = get_file_path()
    file_type = get_file_type(file_path)
    if file_type == constant.IMAGE_TYPE:
       gui.Gui.display_photo(canvas, file_path)
    elif file_type == constant.TEXT_TYPE:
       gui.Gui.display_text(canvas, file_path)

def update_file_index(state):
    global file_index, file_list, file_has_changed

    file_has_changed_lock.acquire()
    file_has_changed = True
    file_has_changed_lock.release()

    if state == constant.INCREMENT and file_index < len(file_list) - 1:
        file_index = file_index + 1
    elif state == constant.DECREMENT:
        if file_index == 0:
          load_file_list()
        if file_index > 0:
          file_index = file_index - 1
    elif state == constant.NEW:
        file_index = 0

def load_file_list():
    global file_list
    # Files are named by date and we want to display newest first
    file_list = sorted(glob.glob(config.PATH))
    file_list.reverse()
    logging.debug("File list is : %s", file_list)

def get_newer_item():
    logging.info("Newer item button was pressed")
    update_file_index(constant.DECREMENT)

def get_older_item():
    logging.info("Older item button was pressed")
    update_file_index(constant.INCREMENT)

def display_new_item():
    logging.info("New item button was pressed")
    load_file_list()
    update_file_index(constant.NEW)
