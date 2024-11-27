from tkinter import *
from time import strftime
import settings
import utils
from minesweeper_cell import Cell

root = Tk()

#create necessary images

flag_img = PhotoImage(file = r"images/flag.png")
mine_img = PhotoImage(file = r"images/mine.png")
happy_img = PhotoImage(file = r"images/happy.png")
sad_img = PhotoImage(file = r"images/sad.png")
heart_img = PhotoImage(file = r"images/heart.png")
empty_img = PhotoImage()

#define seconds counter
def time():
    settings.seconds += 1
    string = str(settings.seconds).zfill(3)
    time_label.config(text=string)
    time_label.after(1000, time)

seconds = 0

#setup root
root.configure(bg=utils._from_rgb(128,128,128))
root.geometry(f"{settings.GAME_WIDTH}x{settings.GAME_HEIGHT}")
root.title('Minesweeper')
root.resizable(False, False)

#setup top frame
top_frame = Frame(
    root,
    bg=utils._from_rgb(169,169,169),
    width=utils._widthPercentage(98),
    height=utils._heightPercentage(15)
)

top_frame.place(
    x=utils._widthPercentage(1), y=utils._heightPercentage(2)
)

#mines counter
Cell.create_mine_count_label(top_frame)
Cell.cell_mines_count.place(
    x=utils._widthPercentage(10),
    y=utils._heightPercentage(3)
)

#reset button
reset_button = utils.create_reset_button(top_frame, happy_img)
reset_button.bind('<Button-1>', Cell.reset)

#time counter
time_label = Label(
    top_frame,
    font = ('ds-digital','30','bold'),
    text="00",
    bg=utils._from_rgb(0,0,0),
    fg=utils._from_rgb(210,43,43)
)
time_label.place(
    x=utils._widthPercentage(80),
    y=utils._heightPercentage(3)
)
time()

#setup cells frame

cells_frame = Frame(
    root,
    bg=utils._from_rgb(169,169,169),
    width=utils._widthPercentage(98),
    height=utils._heightPercentage(79)
)
cells_frame.place(
    x=settings.CELLS_POS,
    y=utils._heightPercentage(19)
)

#setup cells

Cell.reset_button = reset_button
Cell.empty_img = empty_img
Cell.flag_img = flag_img
Cell.mine_img = mine_img
Cell.happy_img = happy_img
Cell.sad_img = sad_img
Cell.heart_img = heart_img

for i in range(settings.GRID_SIZE_W):
    for j in range(settings.GRID_SIZE_H):
        cell = Cell(
            cells_frame,
            i, j, False,
        )

Cell.randomize_mines()

root.mainloop()