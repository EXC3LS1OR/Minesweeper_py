import settings
from tkinter import Button, OptionMenu


def _heightPercentage(percent):
    return int(settings.GAME_HEIGHT * percent / 100)

def _widthPercentage(percent):
    return int(settings.GAME_WIDTH * percent / 100)

def _from_rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def create_reset_button(location, happy_img):
    reset_button = Button(
    location,
    image=happy_img,
    bg=_from_rgb(169,169,169),
    )
    
    reset_button.place(
        x=_widthPercentage(50),
        y=_heightPercentage(3)
    )
    return reset_button

def change_face(reset_button, img):
    if reset_button:
        reset_button.config(image=img)

def create_size_selector(location):
    size_selector = OptionMenu(
        location,
        settings.GRID_SIZE,
        *settings.GRID_SIZES
    )
    size_selector.place(
        x=_widthPercentage(40),
        y=_heightPercentage(3)
    )
    return size_selector
